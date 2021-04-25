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
		<h1>SEARCH</h1>
	</div>
    <div class="card">
    <h5>Evaluation search</h5>
	<p>{{errorstr}}</p>
	<form action="/search" method="get">
		<label for="start">Start date:</label>
		<input type="date" id="eval_start" name="eval_start">
		<label for="start">End date:</label>
		<input type="date" id="eval_end" name="eval_end">
		<input type="submit" value="Search">
	</form>
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

</body>
</html>