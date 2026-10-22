
<html> 
<head>
<meta name="copyright" content="Copyright (C) 2001-2202 Bruce Corkhill">
<TITLE>Discussion Forum Search</TITLE>

<!-- The Web Wiz Guide ASP forum is written by Bruce Corkhill ©2001-2002
    	 If you want your forum then goto http://www.webwizguide.info --> 

<!-- Check the from is filled in correctly before submitting -->
<script  language="JavaScript">
<!-- Hide from older browsers...

//Function to check form is filled in correctly before submitting
function CheckForm () {

	//Check for a somthing to search for
	if (document.frmSearch.search.value==""){
	
		msg = "_______________________________________________________________\n\n";
		msg += "The form has not been submitted because there are problem(s) with the form.\n";
		msg += "Please correct the problem(s) and re-submit the form.\n";
		msg += "_______________________________________________________________\n\n";
		msg += "The following field(s) need to be corrected: -\n";
	
		alert(msg + "\n\tSearch For\t- Enter something to search for\n\n");
		document.frmSearch.search.focus();
		return false;
	}
	
	return true
}
// -->
</script>


<style type="text/css">
<!--
.text {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 12px; color: #000000;}
.bold {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 12px; color: #000000; font-weight: bold;}
.heading {font-family: Arial, Helvetica, sans-serif; font-size: 18px; color: #000000;}
.lgText {font-family: Arial, Helvetica, sans-serif; font-size: 15px; color: #000000; font-weight: bold;}
.tHeading {font-family: Arial, Helvetica, sans-serif; font-size: 12px; color: #000000; font-weight: bold;}
.tiHeading {font-family: Arial, Helvetica, sans-serif; font-size: 12px; color: #000000; font-weight: bold;}
a {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 12px; color: #0000CC;}
a:hover {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 12px; color: #0000CC;}
a:visited {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 12px; color: #0000CC;}
a:visited:hover {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 12px; color: #FF0000;}
-->
</style>

</head>
<body bgcolor="#CCFFFF" text="#000000" background="" marginheight="0" marginwidth="0" topmargin="0" leftmargin="0" onload="document.frmSearch.search.focus();">
<table width="100%" border="0" cellspacing="0" cellpadding="0">
 <tr> 
  <td colspan="2"><table width="90%" border="0" cellspacing="7" cellpadding="0" align="center">
  <tr> 
    <td width="14%" valign="top">&nbsp;
    <td align="center" width="72%"> 
      

<p align="center">
<applet code="Lake.class" id="Lake" width="366" height="60" align="center">
 
  <param name="image" value="forum_images/titoloforum.jpg">
</applet>
</p>

    <td align="center" width="14%"><a href="http://www.drownedmadonna.com" target="_self" style="font-size: 11px;"> Drowned Madonna</a> 
  </tr>
</table></td>
 </tr>
 <tr> 
  <td width="0%" valign="top"><!-- side bar --></td><td width="100%" valign="top">
<div align="center" class="heading">Discussion Forum Search</div>
<div align="center"><a href="default.asp?ForumID=0" target="_self">Return to the Discussion Forum</a><br>
</div>
<form method="get" name="frmSearch" action="search.asp" onSubmit="return CheckForm();" onReset="return confirm('Are you sure you want to reset the form?');">
    <table width="620" border="0" cellspacing="0" cellpadding="0" align="center" bgcolor="#666666" height="8">
     <tr> 
      <td height="2" width="680"> 
        <table width="100%" border="0" align="center"  height="8" cellpadding="4" cellspacing="1">
          <tr > 
            <td align="left" width="57%" height="2"  bgcolor="#FFCC66" class="tHeading" background="forum_images/barra.jpg">Search For</td>
            <td height="2" width="43%" bgcolor="#FFCC66" class="tHeading" background="forum_images/barra.jpg">Search In</td>
          </tr>
          <tr bgcolor="#FFFFCC" background=""> 
            <td align="left" width="57%"  height="2" bgcolor="#FFFFCC" background=""> 
              <input type="text" name="search" maxlength="35" value="">
              <br>
              <span class="text">Search On&nbsp;: 
              <input type="radio" name="searchMode" value="allwords" CHECKED>All Words 
              <input type="radio" name="searchMode" value="anywords" >Any Words 
              <input type="radio" name="searchMode" value="phrase" >Phrase </span></td>
            
         <td height="2" width="43%" valign="top" background=""> 
          <select name="searchIn">
                <option value="Topic" selected>Topic Subject</option>
                <option value="Thread" >Message Body</option>
                <option value="Author" >Author</option>
              </select>
         </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
  <br>
    <table width="620" border="0" cellspacing="0" cellpadding="0" align="center" bgcolor="#666666" height="8">
     <tr> 
      <td height="24" width="680"> 
        <table width="100%" border="0" align="center"  height="8" cellpadding="4" cellspacing="1">
          <tr > 
            <td align="left" width="57%" height="2"  bgcolor="#FFCC66" class="tHeading" background="forum_images/barra.jpg">Search Forum</td>
            <td height="2" width="43%" bgcolor="#FFCC66" class="tHeading" background="forum_images/barra.jpg">Sort Results By</td>
          </tr>
          <tr bgcolor="#FFFFCC" background=""> 
            <td align="left" width="57%"  height="12" bgcolor="#FFFFCC" background=""> 
              <select name="forum">
			  <option value="0">All Forums</option>
                
<option value=2 >Discussioni di carattere generale</option>
<option value=3 >Survivors</option>
<option value=4 >Cerco, vendo o scambio</option>
<option value=9 >Promuovete i vostri siti</option>
<option value=7 >General Discussions</option>
<option value=13 >Promote Your Webpage</option>
<option value=8 >Problems with the Forum</option>
              </select>
            </td>
            
         <td height="12" width="43%" valign="top" background=""> 
          <select name="searchSort">
                <option value="dateDESC" selected>Last Post Time</option>
                <option value="dateASC" >Topic Start Date</option>
                <option value="topic" >Subject Alphabetically</option>
                <option value="views" >Number of Views</option>
              </select>
         </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
  <br>
  <table width="98%" border="0" cellspacing="0" cellpadding="1" align="center">
    <tr>
      <td align="center"> 
        <input type="submit" name="Submit" value="Start Search">
        <input type="reset" name="Reset" value="Reset Form">
      </td>
    </tr>
  </table>
</form>
<div align="center">
<span class="text" style="font-size:10px">Powered by <a href="http://www.webwizguide.info" target="_blank" style="font-size:10px">Web Wiz Forums</a> version 6.11</span><br><span class="text" style="font-size:10px">Copyright &copy;2001-2002 Web Wiz Guide</span>
</div>
</td>
 </tr>
 <tr> 
  <td colspan="2"> <!-- footer -->
 <br> </td>
 </tr>
</table>
</body>
</html>