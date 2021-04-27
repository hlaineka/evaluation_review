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
  <a href="/index" style="float:left">Home</a>
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
		<h1>STUDENTS</h1>
	</div>
    <div class="card">
      {{!students}}
    </div>
  </div>
  <div class="rightcolumn">
    <div class="card3">
      <h2>Evaluation Reviewer</h2>
      <p><a href="/index#basic">Info about the app</a></p>
      <p><a href="/index#technical">Technical info</a></p>
      <p><a href="/index#eval">Evaluation points</a></p>
      <p><a href="/index#usability">Usability</a></p>
      <p><a href="/index#database">Database structure</a></p>
      <p><a href="/index#process">The process of making this project</a></p>
      <p><a href="/index#ideas">Ideas for the future</a></p>
      <p><a href="/index#other">Other info</a></p>
    </div>
    <div class="card4">
      <h3>About Me</h3>
      <p>This project was created by hlaineka</p>
      <a href="https://github.com/hlaineka/evaluation_review"><img src="images/GitHub-Mark-32px.png"></a>
      <a href="https://www.linkedin.com/in/helvi-lainekallio/"><img src="images/LI-In-Bug.png"></a>
    </div>
  </div>
</div>

<div class="footer">
  <div class="footer_leftcolumn">
  <p style="float:right; position: relative; right:15px; ">This project is made for the use of Hive Helsinki</p>
  </div>
  <div class="footer_rightcolumn">
  <p style="float:left; position: relative; left:15px;">@hlaineka</p>
  </div>
</div>

</body>
</html>