
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <errno.h>
#include <netinet/in.h>
#include <arpa/inet.h>

static char board[9];
static int port = 41001;
static int side = 0;
static int listenfd;

struct client {
    int fd;
    struct client *next;
} *top = NULL;

static void setup();
static void setup_theboard();
static void newconnection();
static void addclient();
static void removeclient();
static void parseforport(int argc, char **argv);
static void process(struct client *p);
static void broadcast(char *s, int size);


char *check_game_over()  /* returns string beginning with '!', or NULL */
{
    int playernum, player, i, j;
    static int basis[] = { 0, 3, 6, 0, 1, 2, 0, 2 };
    static int increment[] = { 1, 1, 1, 3, 3, 3, 4, 2 };

    for (playernum = 0; playernum < 2; playernum++) {
	player = "xo"[playernum];
	for (i = 0; i < sizeof basis / sizeof basis[0]; i++) {
	    for (j = 0;
		    j < 3 && board[basis[i] + j*increment[i]] == player;
		    j++)
		;
	    if (j == 3) {
		switch (player) {
		case 'x':
		    return("!X wins");
		case 'o':
		    return("!O wins");
		}
	    }
	}
    }

    /* Or maybe it's a draw? */
    for (i = 0; i < 9; i++)
	   if (board[i] == 0)
	       return(NULL);
    return("!Draw");
}

int main(int argc, char **argv)
{
    parseforport(argc, argv);
    setup();
    struct client *p;
    //main loop
    while (1){
        fd_set fdlist;
        int maxfd = listenfd;
        FD_ZERO(&fdlist);
        FD_SET(listenfd, &fdlist);
        for (p = top; p; p = p->next) {
            FD_SET(p->fd, &fdlist);
            if (p->fd > maxfd){
                maxfd = p->fd;
            }
        }

        if (select(maxfd + 1, &fdlist, NULL, NULL, NULL) < 0) {
            perror("select");
        } else {
            for (p = top; p; p = p->next){
                if (FD_ISSET(p->fd, &fdlist)){
                    break;
                }
            }
        }
        if (p){
            process(p);
        } 
        if (FD_ISSET(listenfd, &fdlist)){
            newconnection();
        }
    }
    return (0);
}

//setup the server
static void setup()  
{
    struct sockaddr_in r;

    listenfd = socket(AF_INET, SOCK_STREAM, 0);

    r.sin_family = AF_INET;
    r.sin_addr.s_addr = INADDR_ANY;
    r.sin_port = htons(port);

    if (bind(listenfd, (struct sockaddr *)&r, sizeof r)) {
        perror("bind");
        exit(1);
    }

    if (listen(listenfd, 5)) {
        perror("listen");
        exit(1);
    }
    setup_theboard();
}

//setup the board
static void setup_theboard()
{
    int i;
    for (i = 0; i < 9; i++){
        board[i] = 0;
    }
}
//accept new connection
static void newconnection()  
{
    int fd;
    struct sockaddr_in r;
    socklen_t len = sizeof r;

    if ((fd = accept(listenfd, (struct sockaddr *)&r, &len)) < 0) {
        perror("accept");
    } 
    else {
        static char greeting[] = "ticsvr1\r\n";
        printf("new connection from %s, fd %d\n", inet_ntoa(r.sin_addr), fd);
        fflush(stdout);
        addclient(fd);
        write(fd, greeting, sizeof greeting - 1);
    }
}

//add the client to the linked list when a new 
//connection is established
static void addclient(int fd)
{
    struct client *p = malloc(sizeof(struct client));

    /* Unlikely to happen */
    if (!p) {
        fprintf(stderr, "out of memory!\n"); 
        exit(1);
    }
    p->fd = fd;
    p->next = top;
    top = p;
} 

//remove the client
static void removeclient(struct client *p)
{
    struct client **pp;
    for (pp = &top; *pp && *pp != p; pp = &(*pp)->next)
    ;
    if (*pp) {
        struct client *t = (*pp)->next;
        free(*pp);
        *pp = t;
    } else {
        fprintf(stderr, "Trying to remove the client %d, but the client doesn't exist\n", p->fd);
        fflush(stderr);
    }
}   

//handle -p argument
static void parseforport(int argc, char **argv)
{
    int c;
    while ((c = getopt(argc, argv, "p:")) != EOF) {
        if (c == 'p') {
            if ((port = atoi(optarg)) < 1) {
                fprintf(stderr, "%s: port argument must be greater than 0\n", argv[0]);
                exit(1);
            }
        } else {
            fprintf(stderr, "usage: %s [-p port]\n", argv[0]);
            exit(1);
        }
    }
}

//broadcast the message to all client
static void broadcast(char *s, int size)
{
    struct client *p;
    for (p = top; p; p = p->next){
        write(p->fd, s, size);
    }
}


static void process(struct client *p)  /* select() said activity; check it out */
{
    char buf[80];
    char message[80];
    char *result;
    int len;

    len = read(p->fd, buf, sizeof buf - 1);
    if (len <= 0) {
        if (len < 0){
            perror("read()");
        }
        close(p->fd);
        printf("Disconnecting fd %d \n", p->fd);
        fflush(stdout);
        removeclient(p);
    }

    if (buf[0] == 'c'){
            setup_theboard();
            sprintf(message, "c\r\n");
            broadcast(message, strlen(message));
            side = 0;
    }
    else{   
        result = check_game_over();
        if (result == NULL){
            int index =  atoi(buf);
            if(side == 0 && board[index] == 0){
                board[index] = 'x';
                sprintf(message, "x%d\r\n", index);
                broadcast(message, strlen(message));
                side = 1;
            }else if (side == 1 && board[index] == 0){
                board[index] = 'o';
                sprintf(message, "o%d\r\n", index);
                broadcast(message, strlen(message));
                side = 0;
           }
        }else{
            sprintf(message, "%s\r\n", result);
            broadcast(message, strlen(message));  
        }
    }
}
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
