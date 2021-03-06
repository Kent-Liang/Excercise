/**
 * HTTP Server, Single Threaded,  starter code.  
 * Usage:  java HTTPServer [port#  [http_root_path]]
 **/

import java.io.*;
import java.net.*;
import java.text.SimpleDateFormat;
import java.util.*;

public final class HTTPServer {
    public static int serverPort = 2555;    // default port CHANGE THIS
    public static String http_root_path = "C:\\wamp\\www\\test";    // rooted default path in your mathlab area
    public static String check = null;
    
    public static void main(String args[]) throws Exception  {
    	// ADD_CODE: allow the user to choose a different port, as arg[0]
    	// ADD_CODE: allow the user to choose a different http_root_path, as arg[1] 
        if (args.length >= 1 && isNum(args[0])){
            serverPort = Integer.parseInt(args[0]);
        }
        if (args.length >= 2){
        	http_root_path = args[1];
        }
        // display error on server stdout if usage is incorrect
        if (args.length > 2) {
        	System.out.println("usage: java HTTPServer [port_# [http_root_path]]");
        	System.exit(0);
        }
        ServerSocket serverSocket = null;
        Socket clientSocket = null;
        // ADD_CODE: create server socket 
        try 
        {
        	serverSocket = new ServerSocket(serverPort);
        } 
        catch (IOException e) 
        {
	   System.err.println("Could not listen on port: " + serverPort + ".");
           System.exit(1);
	 }
	// ADD_CODE: display server stdout message indicating listening
	// on port # with server root path ... 
	System.out.println("Listening on " + serverPort + " with " + http_root_path);
	
	// server runs continuously
	while (true) {
	    try {
		// ADD_CODE: take a waiting connection from the accepted queue 
	    	clientSocket =  serverSocket.accept(); 
		// ADD_CODE: display on server stdout the request origin  
	    	System.out.println("Connection from " 
					+ clientSocket.getInetAddress() + "." 
					+ clientSocket.getPort());
		/* you may wish to factor out the remainder of this
		 * try-block code as a helper method, that could be used
		 * by your multi-threaded solution, since it will require
		 * essentially the same logic for its threads.
		 */

		// create buffered reader for client input 	// ADD_CODE
 		BufferedReader inFromClient = new BufferedReader
				(new InputStreamReader(clientSocket.getInputStream())); 
		PrintWriter output = new PrintWriter(
			     new OutputStreamWriter(clientSocket.getOutputStream()));
		String requestLine = null;	// the HTTP request line
		String requestHeader = null;	// HTTP request header line

		/* Read the HTTP request line and display it on Server stdout.
		 * We will handle the request line below, but first, read and
		 * print to stdout any request headers (which we will ignore).
		 */
                requestLine = inFromClient.readLine();  // ADD_CODE
        
                System.out.println(requestLine);
                
                /*try{
                    requestHeader = inFromClient.readLine();
                    check = requestHeader.substring(requestHeader.indexOf(":"));
                }catch (Exception e){
                    continue;
                }*/

		// now back to the request line; tokenize the request
		StringTokenizer tokenizedLine = new StringTokenizer(requestLine);
		// process the request
                
		if (tokenizedLine.nextToken().equals("GET")) {
		    String urlName = null;	    
		    // parse URL to retrieve file name
		    urlName = tokenizedLine.nextToken();
	    
		    if (urlName.startsWith("/") == true )
		    	urlName  = urlName.substring(1);
		    
		    generateResponse(urlName, clientSocket);

		} 
		else 
		    System.out.println("Bad Request Message");
	    } catch (Exception e) {
                System.err.println("Error: " + e);
            }
	}  // end while true 
	
    } // end main
    private static boolean isNum(String S){
        //Check wether or not the string is a number
    	try {  
            double d = Double.parseDouble(S);  
    	}  
    	catch(NumberFormatException e){   
    	    return false;  
    	}  
    	return true;  
    }
    private static String getContentType(String fileloc){
        //Get the content type of the file
    	if (fileloc.endsWith(".html")||fileloc.endsWith(".htm") ){
    		return "text/html";
    	}
    	else if (fileloc.endsWith(".css")){
    		return "text/css";
    	}
    	else if (fileloc.endsWith(".js")){
    		return "text/javascript";
    	}
    	else if (fileloc.endsWith(".jpg") ||
    		      fileloc.endsWith(".jpeg")){
    		return "image/jpeg";
    	}
    	else{
    		return "text/plain";
    	}
    }
    private static void generateResponse(String urlName, Socket connectionSocket) throws Exception
    {
	// ADD_CODE: create an output stream 
    	DataOutputStream outToClient = new DataOutputStream(connectionSocket.getOutputStream());

        //Assume there is a slash at the end of root path
    	String fileLoc = http_root_path + urlName;// ADD_CODE: map urlName to rooted path  
    	System.out.println ("Request Line: GET " + fileLoc);

        File file = new File( fileLoc );

        if (!file.isFile())
    	{
    		// generate 404 File Not Found response header
    		outToClient.writeBytes("HTTP/1.0 404 File Not Found\r\n");
    		// and output a copy to server's stdout
    		System.out.println ("HTTP/1.0 404 File Not Found\r\n");
    	} else {
    		// get the requested file content
    		int numOfBytes = (int) file.length();
	    
    		FileInputStream inFile  = new FileInputStream (fileLoc);
	
    		byte[] fileInBytes = new byte[numOfBytes];
    		inFile.read(fileInBytes);
    		
    		String content = getContentType(fileLoc);
    		SimpleDateFormat f = new SimpleDateFormat("dd-MMM-yyyy");

                if (check != null && f.parse(check).getTime() > file.lastModified()){ 
                    System.out.println("HTTP/1.0 304 Not Modified");
                }else{
                
                    // ADD_CODE: generate HTTP response line; output to stdout
                    System.out.println("HTTP/1.0 200 OK");
                    // ADD_CODE: generate HTTP Content-Type response header; output to stdout
                    System.out.println("Content-type: " + content);
                    // ADD_CODE: generate HTTP Content-Length response header; output to stdout
                    System.out.println("Content-length: " + numOfBytes);
                    System.out.println("");
                    // send file content
                    outToClient.write(fileInBytes, 0, numOfBytes);
                    inFile.close();	
                }
            }// end else (file found case)
	// close connectionSocket
	connectionSocket.close();
    } // end of generateResponse
    
} // end of class HTTPServer
