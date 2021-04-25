<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="/static/{{style}}">
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
		<h1>EVALUATION</h1>
	</div>
    <div class="card">
		<p>Project name: {{project_name}}</p>
		<p>Corrector: {{corrector}}</p>
		<p>Correcteds: {{correcteds}}<p>
		<p>Too friendly points: NOT ADDED</p>
		<p>Comment: {{comment}}</p>
		<p>Comment points: {{comment_points}}</p>
		<p>Final mark: {{final_mark}}</p>
		<p>Final mark points: {{final_mark_points}}</p>
		<p>Begin at: {{begin_at}}</p>
		<p>Duration (in seconds): {{duration}}</p>
		<p>Duration points: {{duration_points}}</p>
		<p>Flags points: NOT ADDED</p>
		<p>Feedback comment: {{feedback_comment}}</p>
		<p>Feedback rating (max 12): {{feedback_rating}}</p>
		<p>Feedback points: {{feedback_points}}</p>
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
  <p style="float:left">@hlaineka</p>
  </div>
</div>

</body>
</html>