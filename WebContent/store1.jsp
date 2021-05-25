<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<%@page import="java.sql.DriverManager"%>
<%@page import="java.sql.PreparedStatement"%>
<%@page import="java.sql.Statement"%>
<%@page import="java.sql.Connection"%>
<%

String driver = "com.mysql.jdbc.Driver";
String connectionUrl = "jdbc:mysql://127.0.0.1:3306/netflix";

String userid = "root";
String password = "ibrahim";
try {
Class.forName(driver);
} catch (ClassNotFoundException e) {
e.printStackTrace();
}
Connection connection = null;
Statement statement = null;

%>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="netflix.css">
    <title>Review Hub</title>
</head>
<body>
    <header class="showcase">
        
<%
String hotel=request.getParameter("hotel");
String date=request.getParameter("date");
String time=request.getParameter("time");
String persons=request.getParameter("persons");
String name=request.getParameter("name");
String mail=request.getParameter("email");
String phone=request.getParameter("phone");
try{
	Class.forName("com.mysql.jdbc.Driver");
    
    
    //creating connection with the database 
    Connection con = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/netflix","root","ibrahim");

    PreparedStatement ps = con.prepareStatement("insert into netflix.reviewhub values(?,?,?,?,?,?,?)");
   

    ps.setString(1, hotel);
    ps.setString(2, date);
    ps.setString(3, time);
    ps.setString(4, persons);
    ps.setString(5, name);
    ps.setString(6, mail);
    ps.setString(7, phone);
    
    int i = ps.executeUpdate();
    
    
    if(i > 0) {
    	response.sendRedirect("reservation.jsp"); 
    }}
catch (Exception e) {
e.printStackTrace();%>

<div class="showcase-content">
<center>
		<h3>sorry<%=name %>there is an error in booking</h3>
	           </center>

</div><%
}
%>

</body>
</html>