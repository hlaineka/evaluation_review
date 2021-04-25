<!DOCTYPE html>
<html>
<head>
%
<link rel="stylesheet" href="static/{{style}}">
%end
</head>
<body>
<div class="topnav">
  <div class="topnav_leftcolumn">
	<a href="/evals" style="float:right">Evaluations</a>
	<a href="/students" style="float:right">Students</a>
  </div>
  <div class="topnav_rightcolumn">
  <a href="/search" style="float:left">Search</a>
  </div>
</div>
<div class="row">
	<div class="leftcolumn">
	<div class="card2">
		<h1>EVALUATION REVIEWER</h1>
	</div>
    <div class="card">
     <div id="content">
	    <h2>DATABASE CREATION</h2>
			<p>Before you can use the app, you need to create the database. It will take some time!</p>
			  <form action="http://localhost:6660" method="post" id="button" class="submit_form">
        <input class="submit" type="submit" name="start" value="Create Database" />
        </form>
        <br>
        <br>
        <br>
        <br>
        <br>
     </div>
    <div id="loading">
    <h3>Unicorns are burbing life into the database!</h3>
    %
    <img src="images/{{picture}}">
    %end
    </div>
    </div>
  </div>
  <div class="rightcolumn">
    <div class="card3">
      <h2>About Me</h2>
      <p>This project was created by hlaineka</p>
    </div>
    <div class="card4">
      <h3>Follow Me</h3>
      <p>Some text..</p>
    </div>
  </div>
</div>

<div class="footer">
  <div class="footer_leftcolumn">
  <p style="float:right; position: relative; right:15px; ">This project is made for the use of Hive Helsinki</p>
  </div>
  <div class="footer_rightcolumn">
  <p style="float:left position: relative; left:15px;">@hlaineka</p>
  </div>
</div>

<script type="text/javascript">
  function unicorns(){
      document.getElementById("loading").style.display = "block";
      document.getElementById("content").style.display = "none";
   }
   function init(){
     document.getElementById("loading").style.display = "none";
      document.getElementById("content").style.display = "block";
      document.getElementById("button").onsubmit = unicorns;
   }
   window.onload = init;
</script>
</body>
</html>
