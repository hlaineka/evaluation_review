<!DOCTYPE html>
<html>
<head>
%
<link rel="stylesheet" href="static/{{style}}">
%end
</head>
<body>
<div class="header">
	<h1>Evaluation reviewer</h1>
</div>
<div class="topnav">
</div>
<div class="row">
	<div class="leftcolumn">
	<div class="card">
   <div id="content">
		<h2>DATABASE CREATION</h2>
			<p>Before you can use the app, you need to create the database. It will take some time!</p>
			  <form action="http://localhost:6660" method="post" id="button" class="submit_form">
        <input class="submit" type="submit" name="start" value="Create Database" />
        </form>
    </div>
    <div id="loading">
    %
     <img src="images/{{picture}}">
     %end
    </div>
  </div>
  </div>
  <div class="rightcolumn">
    <div class="card">
      <h2>About Me</h2>
      <p>This project was created by hlaineka</p>
    </div>
    <div class="card">
      <h3>Follow Me</h3>
      <p>Some text..</p>
    </div>
  </div>
</div>

<div class="footer">
  <h2>Footer</h2>
</div>
<script type="text/javascript">
  function unicorns(){
      document.getElementById("loading").style.display = "block";
      document.getElementById("content").style.display = "none";
   }
   function init(){
      document.getElementById("button").onsubmit = unicorns;
   }
   window.onload = init;
</script>
</body>
</html>