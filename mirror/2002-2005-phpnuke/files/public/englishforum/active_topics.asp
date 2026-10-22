
<html>
<head>
<meta name="copyright" content="Copyright (C) 2001-2202 Bruce Corkhill">
<title>Discussion Forum: Active Topics</title>

<!-- Web Wiz Forums is written and produced by Bruce Corkhill ©2001-2002
     	If you want your own Forum then goto http://www.webwizguide.info -->
     	
<script  language="JavaScript">
<!-- Hide from older browsers...

//Function to choose how many topics are show
function ShowTopics(Show){

   	strShow = escape(Show.options[Show.selectedIndex].value);
   	
   	if (Show != "") self.location.href = "active_topics.asp?PagePosition=1&showActive=" + strShow;
	return true;
}

//Function to jump to another forum
function ForumJump(URL) {
	
	if (URL.options[URL.selectedIndex].value != "") self.location.href = URL.options[URL.selectedIndex].value;	
	return true;
}

//Function to open pop up window
function openWin(theURL,winName,features) {
  	window.open(theURL,winName,features);
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
<body bgcolor="#CCFFFF" text="#000000" background="" marginheight="0" marginwidth="0" topmargin="0" leftmargin="0">
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
  <td width="0%" valign="top"><!-- side bar --></td>
  <td width="100%" valign="top">
<br>
<table width="98%" border="0" cellspacing="0" cellpadding="3" align="center">
 <tr> 
  <td class="text">Welcome Guest</td>
  <td align="right">
<a href="register_form.asp?ReturnPage=Active&PagePosition=1" target="_self"><img src="forum_images/register.gif" width="87" height="26" alt="Register" border="0" align="absmiddle"></a>&nbsp;<a href="login_user.asp?ReturnPage=Active&ForumID=&PagePosition=1" target="_self"><img src="forum_images/login.gif" width="87" height="26" alt="Login" border="0" align="absmiddle"></a>
   <a href="search_form.asp?ReturnPage=Active&PagePosition=1" target="_self"><img src="forum_images/search.gif" width="87" height="26" align="absmiddle" border="0" alt="Search The Forum"></a> 
   <a href="forum_members.asp?ReturnPage=Active&PagePosition=1" target="_self"><img src="forum_images/members_list.gif" width="87" height="26" border="0" align="absmiddle" alt="Display List of Forum Members"></a></td>
 </tr>
</table>
<a href="http://www.webwizguide.info"></a> 
<table width="98%" border="0" cellspacing="0" cellpadding="3" align="center">
 <tr> 
  <td align="left" width="71%"><img src="forum_images/folder_icon.gif" border="0" align="bottom">&nbsp;<a href="default.asp" target="_self">All Forums</a><br>
            <img src="forum_images/folder_line.gif">&nbsp;<img src="forum_images/open_folder_icon.gif"> 
            <a href="active_topics.asp" target="_self">Active Topics</a></td>
  <td align="right" width="29%">&nbsp; 
   </td>
 </tr>
</table>
      <table width="98%" border="0" cellspacing="0" cellpadding="4" align="center">
        <tr> 
          <form>
            <td><span class="text">Show Active Topics since</span> 
              <select name="show" onChange=ShowTopics(this)>
                <option value="1" >Last visit on 13 Ottobre 2002 at 12:25</option>
                <option value="2" >Last 15 minutes</option>
                <option value="3" >Last 30 minutes</option>
                <option value="4" >Last 45 minutes</option>
                <option value="5" >Last hour</option>
                <option value="6" >Last 2 hours</option>
                <option value="7" selected>Yesterday</option>
                <option value="8" >from the Last Week</option>
                <option value="9" >from the Last Month</option>
              </select>
            </td>
          </form>
        </tr>
      </table>
<table width="98%" border="0" cellspacing="0" cellpadding="0" bgcolor="#666666" align="center">
 <tr> 
  <td> 
   <table width="100%" border="0" cellspacing="1" cellpadding="2" height="14" bgcolor="#666666">
    <tr> 
     <td bgcolor="#FFCC66" width="3%" height="2" class="tHeading" background="forum_images/barra.jpg">&nbsp;</td>
     <td bgcolor="#FFCC66" width="41%" height="2" class="tHeading" background="forum_images/barra.jpg">Topics</td>
     <td bgcolor="#FFCC66" width="15%" height="2" class="tHeading" background="forum_images/barra.jpg">Topic Starter</td>
     <td bgcolor="#FFCC66" width="7%" align="center" height="2" class="tHeading" background="forum_images/barra.jpg">Replies</td>
     <td bgcolor="#FFCC66" width="7%" align="center" height="2" class="tHeading" background="forum_images/barra.jpg">Views</td>
     <td bgcolor="#FFCC66" width="29%" align="center" height="2" class="tHeading" background="forum_images/barra.jpg">Last Post</td>
    </tr>
    
<td bgcolor="#CCCCFF" background="" colspan="6" class="tiHeading">Discussioni di carattere generale</td>
    <tr> 
     <td bgcolor="#F8F7EF" background="" width="1%" align="center"><img src="forum_images/no_new_posts_icon.gif" border="0" alt="Open Topic (no new replies)"></td>
     <td bgcolor="#F8F7EF" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2165&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">1 canz&#111;ne da ogni album!</a></td>
     <td bgcolor="#F8F7EF" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=22&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">*cosmic*system*</a></td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">2</td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">11</td>
     <td bgcolor="#F8F7EF" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;12:24
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=24&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">unconscious</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2165&PagePosition=1&get=last#14826" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#FEFEFC" background="" width="1%" align="center"><img src="forum_images/pinned_topic_icon.gif" border="0" alt="Pinned Topic"></td>
     <td bgcolor="#FEFEFC" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2074&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">Il nuovo album: EIN SOF?</a><br><img src="forum_images/pages_icon.gif" align="middle" alt="Pages"> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2074&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">1</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2074&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">2</a></td>
     <td bgcolor="#FEFEFC" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=11&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">Immaculate Too</a></td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">13</td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">174</td>
     <td bgcolor="#FEFEFC" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;12:18
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=57&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">elemaddy85</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2074&PagePosition=1&get=last#14825" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#F8F7EF" background="" width="1%" align="center"><img src="forum_images/pinned_topic_icon.gif" border="0" alt="Pinned Topic"></td>
     <td bgcolor="#F8F7EF" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2022&PagePosition=1&showActive=7&ReturnPage=Active" target="_self"> SUSAN  - VOTA LA TUA SCENA PREFERITA!!!</a><br><img src="forum_images/pages_icon.gif" align="middle" alt="Pages"> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2022&PagePosition=1&ThreadPage=4&showActive=7" target="_self" style="font-size:10px;">1</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2022&PagePosition=1&ThreadPage=4&showActive=7" target="_self" style="font-size:10px;">2</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2022&PagePosition=1&ThreadPage=4&showActive=7" target="_self" style="font-size:10px;">3</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2022&PagePosition=1&ThreadPage=4&showActive=7" target="_self" style="font-size:10px;">4</a></td>
     <td bgcolor="#F8F7EF" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=11&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">Immaculate Too</a></td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">31</td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">311</td>
     <td bgcolor="#F8F7EF" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;12:11
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=57&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">elemaddy85</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2022&PagePosition=1&get=last#14824" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#FEFEFC" background="" width="1%" align="center"><img src="forum_images/no_new_posts_icon.gif" border="0" alt="Open Topic (no new replies)"></td>
     <td bgcolor="#FEFEFC" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2164&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">MEZZA FACCIATA PER IL DISGUSTOSO FILM!</a></td>
     <td bgcolor="#FEFEFC" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=22&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">*cosmic*system*</a></td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">2</td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">10</td>
     <td bgcolor="#FEFEFC" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;12:09
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=24&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">unconscious</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2164&PagePosition=1&get=last#14823" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#F8F7EF" background="" width="1%" align="center"><img src="forum_images/no_new_posts_icon.gif" border="0" alt="Open Topic (no new replies)"></td>
     <td bgcolor="#F8F7EF" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2163&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">DAD &#111;n charts --v. 1.1--</a></td>
     <td bgcolor="#F8F7EF" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=62&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">MedardO)(MariO</a></td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">2</td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">17</td>
     <td bgcolor="#F8F7EF" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;12:02
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=24&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">unconscious</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2163&PagePosition=1&get=last#14820" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#FEFEFC" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#FEFEFC" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2162&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">AIUTATEMIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII</a><br><img src="forum_images/pages_icon.gif" align="middle" alt="Pages"> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2162&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">1</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2162&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">2</a></td>
     <td bgcolor="#FEFEFC" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=24&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">unconscious</a></td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">18</td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">49</td>
     <td bgcolor="#FEFEFC" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;12:00
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=57&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">elemaddy85</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2162&PagePosition=1&get=last#14819" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#F8F7EF" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#F8F7EF" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=1980&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">BBB.....BOWIE</a><br><img src="forum_images/pages_icon.gif" align="middle" alt="Pages"> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=1980&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">1</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=1980&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">2</a></td>
     <td bgcolor="#F8F7EF" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=24&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">unconscious</a></td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">12</td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">67</td>
     <td bgcolor="#F8F7EF" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;10:53
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=24&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">unconscious</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=1980&PagePosition=1&get=last#14796" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#FEFEFC" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#FEFEFC" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2044&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">Larry King Show su cnn</a><br><img src="forum_images/pages_icon.gif" align="middle" alt="Pages"> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2044&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">1</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2044&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">2</a></td>
     <td bgcolor="#FEFEFC" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=229&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">bjorn</a></td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">10</td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">99</td>
     <td bgcolor="#FEFEFC" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;10:51
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=62&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">MedardO)(MariO</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2044&PagePosition=1&get=last#14794" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#F8F7EF" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#F8F7EF" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2043&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">M &amp; M</a><br><img src="forum_images/pages_icon.gif" align="middle" alt="Pages"> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2043&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">1</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2043&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">2</a></td>
     <td bgcolor="#F8F7EF" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=26&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">neeno</a></td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">19</td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">137</td>
     <td bgcolor="#F8F7EF" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;10:48
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=24&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">unconscious</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2043&PagePosition=1&get=last#14792" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#FEFEFC" background="" width="1%" align="center"><img src="forum_images/pinned_topic_icon.gif" border="0" alt="Pinned Topic"></td>
     <td bgcolor="#FEFEFC" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2095&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">Download:DIEANOTHERDAY  video+making of</a></td>
     <td bgcolor="#FEFEFC" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=21&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">mo_webo</a></td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">4</td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">61</td>
     <td bgcolor="#FEFEFC" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;09:58
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=24&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">unconscious</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2095&PagePosition=1&get=last#14785" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#F8F7EF" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#F8F7EF" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2133&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">MAZZIE STAR-FADE INTO YOU!!!!!</a><br><img src="forum_images/pages_icon.gif" align="middle" alt="Pages"> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2133&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">1</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2133&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">2</a></td>
     <td bgcolor="#F8F7EF" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=22&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">*cosmic*system*</a></td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">15</td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">91</td>
     <td bgcolor="#F8F7EF" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;09:54
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=24&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">unconscious</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2133&PagePosition=1&get=last#14784" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#FEFEFC" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#FEFEFC" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2147&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">plastica 10 anni di meno!!???</a><br><img src="forum_images/pages_icon.gif" align="middle" alt="Pages"> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2147&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">1</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2147&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">2</a></td>
     <td bgcolor="#FEFEFC" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=227&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">rayboy</a></td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">11</td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">79</td>
     <td bgcolor="#FEFEFC" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;09:47
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=24&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">unconscious</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2147&PagePosition=1&get=last#14783" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#F8F7EF" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#F8F7EF" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2143&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">la Repubblica su Swept Away</a></td>
     <td bgcolor="#F8F7EF" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=586&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">Sugo</a></td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">6</td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">56</td>
     <td bgcolor="#F8F7EF" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;09:42
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=24&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">unconscious</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2143&PagePosition=1&get=last#14782" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#FEFEFC" background="" width="1%" align="center"><img src="forum_images/no_new_posts_icon.gif" border="0" alt="Open Topic (no new replies)"></td>
     <td bgcolor="#FEFEFC" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2161&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">download:remixes mp3</a></td>
     <td bgcolor="#FEFEFC" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=21&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">mo_webo</a></td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">0</td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">9</td>
     <td bgcolor="#FEFEFC" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;09:41
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=21&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">mo_webo</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2161&PagePosition=1&get=last#14781" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#F8F7EF" background="" width="1%" align="center"><img src="forum_images/pinned_topic_icon.gif" border="0" alt="Pinned Topic"></td>
     <td bgcolor="#F8F7EF" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2146&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">Foto dalla c&#111;nferenza stampa di SweptAway</a></td>
     <td bgcolor="#F8F7EF" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=21&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">mo_webo</a></td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">8</td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">70</td>
     <td bgcolor="#F8F7EF" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;09:40
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=57&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">elemaddy85</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2146&PagePosition=1&get=last#14780" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#FEFEFC" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#FEFEFC" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2152&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">Guardate 1 pò qui......</a></td>
     <td bgcolor="#FEFEFC" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=18&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">Slugaholic86</a></td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">7</td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">64</td>
     <td bgcolor="#FEFEFC" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;09:38
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=57&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">elemaddy85</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2152&PagePosition=1&get=last#14779" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#F8F7EF" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#F8F7EF" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2154&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">DAD:scoprire i simboli...</a></td>
     <td bgcolor="#F8F7EF" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=453&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">pogicon</a></td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">3</td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">27</td>
     <td bgcolor="#F8F7EF" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;09:27
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=57&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">elemaddy85</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2154&PagePosition=1&get=last#14777" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#FEFEFC" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#FEFEFC" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2138&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">Larry King Live-Interview with M and Guy</a></td>
     <td bgcolor="#FEFEFC" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=57&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">elemaddy85</a></td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">2</td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">24</td>
     <td bgcolor="#FEFEFC" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;09:24
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=57&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">elemaddy85</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2138&PagePosition=1&get=last#14776" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#F8F7EF" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#F8F7EF" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2061&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">FIRME</a><br><img src="forum_images/pages_icon.gif" align="middle" alt="Pages"> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2061&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">1</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2061&PagePosition=1&ThreadPage=2&showActive=7" target="_self" style="font-size:10px;">2</a></td>
     <td bgcolor="#F8F7EF" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=25&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">LIZ_</a></td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">19</td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">123</td>
     <td bgcolor="#F8F7EF" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;09:20
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=57&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">elemaddy85</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2061&PagePosition=1&get=last#14775" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#FEFEFC" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#FEFEFC" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=1290&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">I FILM DEI MAD&#079;NNARI</a><br><img src="forum_images/pages_icon.gif" align="middle" alt="Pages"> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=1290&PagePosition=1&ThreadPage=12&showActive=7" target="_self" style="font-size:10px;">1</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=1290&PagePosition=1&ThreadPage=12&showActive=7" target="_self" style="font-size:10px;">2</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=1290&PagePosition=1&ThreadPage=12&showActive=7" target="_self" style="font-size:10px;">3</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=1290&PagePosition=1&ThreadPage=12&showActive=7" target="_self" style="font-size:10px;">4</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=1290&PagePosition=1&ThreadPage=12&showActive=7" target="_self" style="font-size:10px;">5</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=1290&PagePosition=1&ThreadPage=12&showActive=7" target="_self" style="font-size:10px;">6</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=1290&PagePosition=1&ThreadPage=12&showActive=7" target="_self" style="font-size:10px;">7</a> ...<a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=1290&PagePosition=1&ThreadPage=12&showActive=7" target="_self" style="font-size:10px;">12</a></td>
     <td bgcolor="#FEFEFC" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=478&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">tattva</a></td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">119</td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">713</td>
     <td bgcolor="#FEFEFC" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;02:16
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=258&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">soonerorlater</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=1290&PagePosition=1&get=last#14774" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#F8F7EF" background="" width="1%" align="center"><img src="forum_images/no_new_posts_icon.gif" border="0" alt="Open Topic (no new replies)"></td>
     <td bgcolor="#F8F7EF" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2160&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">Mad&#111;nna e i il Botox</a></td>
     <td bgcolor="#F8F7EF" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=47&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">tyger</a></td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">0</td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">6</td>
     <td bgcolor="#F8F7EF" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;02:09
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=47&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">tyger</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2160&PagePosition=1&get=last#14773" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#FEFEFC" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#FEFEFC" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2131&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">EBRAISMO E KABBALA</a></td>
     <td bgcolor="#FEFEFC" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=568&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">Skin Bruno</a></td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">8</td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">43</td>
     <td bgcolor="#FEFEFC" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;02:08
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=258&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">soonerorlater</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2131&PagePosition=1&get=last#14772" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#F8F7EF" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#F8F7EF" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2153&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">PER IOM</a></td>
     <td bgcolor="#F8F7EF" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=478&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">tattva</a></td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">5</td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">37</td>
     <td bgcolor="#F8F7EF" background="" width="29%" class="text" align="right">13 Ottobre 2002&nbsp;at&nbsp;01:39
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=568&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">Skin Bruno</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2153&PagePosition=1&get=last#14768" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#FEFEFC" background="" width="1%" align="center"><img src="forum_images/hot_topic_no_new_posts_icon.gif" border="0" alt="Hot Topic (no new replies)"></td>
     <td bgcolor="#FEFEFC" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2124&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">bl&#111;nd ambiti&#111;n roma foto</a></td>
     <td bgcolor="#FEFEFC" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=386&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">rarità</a></td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">4</td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">38</td>
     <td bgcolor="#FEFEFC" background="" width="29%" class="text" align="right">12 Ottobre 2002&nbsp;at&nbsp;22:29
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=386&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">rarità</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2124&PagePosition=1&get=last#14760" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#F8F7EF" background="" width="1%" align="center"><img src="forum_images/no_new_posts_icon.gif" border="0" alt="Open Topic (no new replies)"></td>
     <td bgcolor="#F8F7EF" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2159&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">classifica remix n&#111;n ufficiali</a></td>
     <td bgcolor="#F8F7EF" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=113&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">mynameisdita</a></td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">0</td>
     <td bgcolor="#F8F7EF" background="" width="7%" align="center" class="text">6</td>
     <td bgcolor="#F8F7EF" background="" width="29%" class="text" align="right">12 Ottobre 2002&nbsp;at&nbsp;22:16
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=113&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">mynameisdita</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2159&PagePosition=1&get=last#14759" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
    <tr> 
     <td bgcolor="#FEFEFC" background="" width="1%" align="center"><img src="forum_images/no_new_posts_icon.gif" border="0" alt="Open Topic (no new replies)"></td>
     <td bgcolor="#FEFEFC" background="" width="41%" class="text"><a href="display_topic_threads.asp?ForumID=2&TopicID=2158&PagePosition=1&showActive=7&ReturnPage=Active" target="_self">nuovi remix mp3</a></td>
     <td bgcolor="#FEFEFC" background="" width="15%" class="text"><a href="JavaScript:openWin('pop_up_profile.asp?profile=113&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">mynameisdita</a></td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">0</td>
     <td bgcolor="#FEFEFC" background="" width="7%" align="center" class="text">12</td>
     <td bgcolor="#FEFEFC" background="" width="29%" class="text" align="right">12 Ottobre 2002&nbsp;at&nbsp;22:00
      <br>By <a href="JavaScript:openWin('pop_up_profile.asp?profile=113&ForumID=2','profile','toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=1,width=440,height=370')">mynameisdita</a> <a href="display_topic_threads.asp?ReturnPage=Active&ForumID=2&TopicID=2158&PagePosition=1&get=last#14758" target="_self"><img src="forum_images/right_arrow.gif" align="absmiddle" border="0" alt="View Last Post"></a></td>
    </tr>
   </table>
  </td>
 </tr>
</table>
<br>
<form>
        <table width="98%" border="0" cellspacing="0" cellpadding="4" align="center">
          <tr> 
            <td> 
              
	<span class="text">Forum Jump</span>
	 <select onChange="ForumJump(this)" name="SelectJumpForum">
           <option value="" selected>-- Select Forum --</option>

		<option value="">Italian Section - Forum In Italiano</option>
		<option value="display_forum_topics.asp?ForumID=2">&nbsp;&nbsp;-&nbsp;Discussioni di carattere generale</option>
		<option value="display_forum_topics.asp?ForumID=3">&nbsp;&nbsp;-&nbsp;Survivors</option>
		<option value="display_forum_topics.asp?ForumID=4">&nbsp;&nbsp;-&nbsp;Cerco, vendo o scambio</option>
		<option value="display_forum_topics.asp?ForumID=9">&nbsp;&nbsp;-&nbsp;Promuovete i vostri siti</option>
		<option value="">English Section</option>
		<option value="display_forum_topics.asp?ForumID=7">&nbsp;&nbsp;-&nbsp;General Discussions</option>
		<option value="display_forum_topics.asp?ForumID=13">&nbsp;&nbsp;-&nbsp;Promote Your Webpage</option>
		<option value="display_forum_topics.asp?ForumID=8">&nbsp;&nbsp;-&nbsp;Problems with the Forum</option>
         </select>
            </td>
            
		<td><span class="text">Page
		 <select onChange="ForumJump(this)" name="SelectTopicPage">
		  <option value="active_topics.asp?PagePosition=1&showActive=7" selected>1</option>
		  <option value="active_topics.asp?PagePosition=2&showActive=7">2</option>
		</select> of 2</span></td>
          </tr>
        </table>
</form>
<div align="center">
 <table width="617" border="0" cellspacing="0" cellpadding="2">
  <tr> 
   <td width="193" class="text"><img src="forum_images/no_new_posts_icon.gif" alt="Open Topic (no new replies)"> <span style="font-size: 10px;"> Open Topic (no new replies)</span></td>
   <td width="184" class="text"><img src="forum_images/hot_topic_no_new_posts_icon.gif" alt="Hot Topic (no new replies)"> <span style="font-size: 10px;"> Hot Topic (no new replies)</span></td>
   <td width="141" class="text"><img src="forum_images/priority_post_icon.gif" alt="Priority Topic"> <span style="font-size: 10px;"> Priority Topic</span></td>
   <td width="94" class="text"><img src="forum_images/pinned_topic_icon.gif" alt="Pinned Topic"> <span style="font-size: 10px;"> Pinned Topic</span></td>
  </tr>
  <tr> 
   <td width="193" class="text"><img src="forum_images/new_posts_icon.gif" alt="Open Topic (new replies)"> <span style="font-size: 10px;"> Open Topic (new replies)</span></td>
   <td width="184" class="text"><img src="forum_images/hot_topic_new_posts_icon.gif" alt="Hot Topic (new replies)"> <span style="font-size: 10px;"> Hot Topic (new replies)</span></td>
   <td width="141" class="text"><img src="forum_images/priority_post_locked_icon.gif" alt="Locked Priority Topic"> <span style="font-size: 10px;">Locked Priority Topic</span></td>
   <td width="94" class="text"><img src="forum_images/closed_topic_icon.gif" alt="Closed Topic"> <span style="font-size: 10px;"> Closed Topic</span></td>
  </tr>
 </table>
 <br>
</div>
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