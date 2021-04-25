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
	<a href="/evals">Evaluations</a>
	<a href="/students">Students</a>
	<a href="/search" style="float:right">Search</a>
</div>
<div class="row">
	<div class="leftcolumn">
	<div class="card">
		<h2>STUDENTS</h2>
			<h5>Hive Helsinki</h5>
			% for student in students:
			<a href="student/{{student[1]}}">{{student[1]}}</a>, <a href="{{student[2]}}">intra</a><br>
			%end
    </div>
    <div class="card">
      <h2>TITLE HEADING</h2>
      <h5>Title description, Sep 2, 2017</h5>
      <div class="fakeimg" style="height:200px;">Image</div>
      <p>Some text..</p>
      <p>Sunt in culpa qui officia deserunt mollit anim id est laborum consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco.</p>
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

</body>
</html>