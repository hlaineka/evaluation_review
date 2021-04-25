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

* {
  box-sizing: border-box;
}

body {
  font-family: Arial;
  padding: 10px;
  background: white;
}

/* Header/Blog Title */
.header {
  padding: 30px;
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
	padding-left: 20px;
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
  float: left;
  width: 75%;
}

/* Right column */
.rightcolumn {
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
  }

  .card3 {
	background-color: #a1d4e0;
	padding: 20px;
	margin-top: 50px;
	margin-left: 10%;
	margin-right: 10%;
	text-align: center;
  }

  .card4 {
	background-color: #f5c5c3;
	padding: 20px;
	margin-top: 50px;
	margin-left: 10%;
	margin-right: 10%;
	text-align: center;
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
	padding-left: 20px;
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
}
</style>
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
		<h1>{{student[1]}}</h1>
	</div>
    <div class="card">
      <p>Info about the student</p>
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
