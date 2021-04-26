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
	<p style="float:right">HI</p>
  </div>
  <div class="topnav_rightcolumn">
  <p style="float:left">VE</p>
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
      <p>If you do not want to wait forever for the database to build, select timeframe to fetch evals! If you do not change the timeframe, database will be fetched from april 18. to april 25. of 2021. Longer = bigger queries might exceed the allowed hourly rate for this app</p>
			  <form action="/wait" method="get" id="button">
		      <label for="start">Start date:</label>
		      <input type="date" id="eval_start" name="eval_start" value="2021-04-18">
		      <label for="start">End date:</label>
		      <input type="date" id="eval_end" name="eval_end" value=2021-04-25>
		      <input type="submit" id="button" value="Create database">
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
