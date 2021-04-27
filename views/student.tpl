<!DOCTYPE html>
<html>
<head>
<style>
div#content {

    }

div#loading {
    cursor: wait;
	margin-left: auto;
    margin-right: auto
    }

body {
  font-family: Arial;
  background: white;
  font-family: 'Courier New', Courier, monospace;
}

/* Header/Blog Title */
.header {
  text-align: center;
  background: #ee7801;
}

.header h1 {
  font-size: 50px;
  text-align: center;
}

/* Style the top navigation bar */
.topnav {
  overflow: hidden;
  background-color: #ee7801;
}

.topnav_leftcolumn {
	float: left;
	width: 75%;
  }

  /* Right column */
.topnav_rightcolumn {
	float: left;
	width: 25%;
	background-color: #ffdd03;
  }

.topnav_right {
	float: right;
}

/* Style the topnav links */
.topnav a {
  float: left;
  display: block;
  color: black;
  text-align: center;
  padding: 16px 18px;
  text-decoration: none;
}

/* Change color on hover */
.topnav a:hover {
  background-color: black;
  color: white;
}

/* Create two unequal columns that floats next to each other */
/* Left column */
.leftcolumn {
	box-sizing: border-box;
	float: left;
  width: 75%;
}

/* Right column */
.rightcolumn {
	box-sizing: border-box;
	float: left;
  width: 25%;
  background-color: white;
  padding-left: 20px;
}

/* Fake image */
.fakeimg {
  background-color: #aaa;
  width: 100%;
  padding: 20px;
}

/* Add a card effect for articles */
.card {
	box-sizing: border-box;
	background-color: white;
  padding: 20px;
  margin-top: 20px;
  margin-left: 15%;
  margin-right: 15%;
}

.card2 {
	background-color: white;
	padding: 20px;
	margin-top: 50px;
	margin-left: 25%;
	margin-right: 25%;
	text-align: center;
	box-sizing: border-box;
  }

  .card3 {
	background-color: #a1d4e0;
	padding: 20px;
	margin-top: 50px;
	margin-left: 10%;
	margin-right: 10%;
	text-align: left;
	box-sizing: border-box;
  }

  .card4 {
	background-color: #f5c5c3;
	padding: 20px;
	margin-top: 50px;
	margin-left: 10%;
	margin-right: 10%;
	text-align: center;
	box-sizing: border-box;
	padding-bottom: 20px;
  }

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}

/* Footer */
.footer {
	overflow: hidden;
}

.footer_leftcolumn {
	float: left;
	background-color: #ee7801;
	width: 75%;

  }

  /* Right column */
.footer_rightcolumn {
	float: left;
	width: 25%;
	background-color: #ffdd03;
  }

/* Responsive layout - when the screen is less than 800px wide, make the two columns stack on top of each other instead of next to each other */
@media screen and (max-width: 800px) {
  .leftcolumn, .rightcolumn {
    width: 100%;
    padding: 0;
  }
}

/* Responsive layout - when the screen is less than 400px wide, make the navigation links stack on top of each other instead of next to each other */
@media screen and (max-width: 400px) {
  .topnav a {
    float: none;
    width: 100%;
  }

</style>
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
		{{!html_insert}}
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