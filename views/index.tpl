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
		<h1>EVALUATION REVIEWER</h1>
	</div>
  <div class="card">
   <h2><a name="basic">INFO ABOUT THE APP</a></h2>
Like with everything, machine calculated points only offer data and should not be used as the only evaluation of how the student is doing. All the points calculated here should only be used as collected data that might show some patterns in how the students act, but in the end, the real evaluation of how the student is doing should be done in person. The feedback points give a lot of information about the evaluation, and the purpose of this app is to give some additional measures on how good the evaluation has been.<br><br><br><br>


<h2><a name="technical">TECHNICAL INFO:</a></h2>
The app is run inside a docker container with Debian 10. Docker will build and run using the run.sh script on Linux and macOS machines, but running the script requires docker to be installed on the computer. The script will also open the web interface on the user's preferred application. Docker will install python3 and pip, and download all the needed libraries listed in the requirements.txt<br><br>

The app uses the Bottle python web framework to create web pages as an interface. The bottle is similar to Flask and was selected quite randomly as the web framework. Since Bottle does not have an OAuth request library integrated, the app is using the Hive Helsinki 42API wrapper, included in the intra.py file. I was not able to make post-requests work properly in Bottle, so all the forms on the page are made with GET and redirecting to pages with arguments on the address.<br><br>

The app is currently running on localhost on port 6660. The port was quite randomly selected but differs from 8080 that might cause some problems since other programs might be using the default port. Because the app runs on localhost, the user side of the OAuth process is not secured. <br><br><br><br>

<h2><a name="eval">EVALUATION POINTS:</a></h2>
Evaluation points = total_points = comment_points + final_mark_points + too_firendly_points + duration_points + flags_points + feedback_total_points <br>
Getting more data and using the evaluation reviewer for a longer time would give more information if the points should be emphasized differently. This is the first draft.<br>
- comment_points: 5 points if the comment the evaluator has written is longer than 180 characters (also the length of the Writer's soul achievement comment), 10 points if the comment is longer than 360 characters. The length of the comment can show that the evaluator has put time and effort into the evaluation, but the length of the comment is not emphasized too much.<br>
- final mark points: If the evaluation ended with 0 points, or if the points given by the evaluator were less than the average points given for the user on this try, 5 points are added to the evaluation points. These points are also taken into account when calculating the duration points since the evaluation might have been short because of an error leading to failure early on the evaluation with a 0 final grade. I included this final mark to points since it shows that the person evaluating has been rigorous in the evaluation if the eval has fewer points than other evals of the project, and they might have notices some errors others missed. On the other hand, giving points for students who give the least points might turn the overall atmosphere of the school, so these points are not emphasized and they award only 5 points maximum.<br>
- Duration points: The duration of the evaluation can either add or subtract points from the total points. If the duration of the evaluation is shorter than ~66% of the target time given in the scale of the project evaluation, -42 points are taken from total points. If the duration of the evaluation is shorter than the target time, -10 points are subtracted. Evaluations that lasted over 1,5 times the target time are awarded 20 points and the rest with 10 points. If evaluation lasted a short time but the final mark shows that a failing error was found, the student gets 10 points. I wanted to include duration in the total points since really short evaluations in my opinion can not be rigorous. Also, a long evaluation shows that the evaluator is putting a lot of effort into the evaluation (or, that the target time is somewhat too short for that evaluation. This tool can be used to get data on this factor also!)<br>
- Flags points: This is not yet applied. Flag points award the evaluator from being rigorous enough to find a failing error. More points for finding something others missed. Flag points somewhat overlap with total mark points, so I left the implementation last. Flag points have not been implemented yet.<br>
- Feedback total points: The total points the evaluated gave the evaluator are multiplied by two to form feedback total points. These make a big part of the points since they are at the time the only real feedback we have on the evaluation. In the future, too friendly points might reduce the points a bit, but not too much. The whole review of evaluations can not completely rely on the total feedback points, since I have noticed that some people are reluctant and shy to reduce points from the evaluation feedback.<br><br>

- too-friendly points: Sometimes students get stuck on evaluating only their friends, and it might lead to a situation where more points are given than the project actually deserves. Too-friendly points assign negative points to an evaluation if the person has already evaluated this person too many times. If the pool of peers the person evaluates is too small, the student’s overall points are reduced. Right now the algorithm gives fewer points to Hivers II since they are so few, so some adjustments need to be made. The number of people who can evaluate a project should be taken into account - if those are few, no points should be subtracted. Now the calculation of too friendly points only takes into account the first corrected. <br><br>

Student average points:<br>
Since no single evaluation is really a good measure of the person, the student’s part of the implementation counts the average points of the evaluations the student has made, to give some info on the students who actually might need intervention about their evaluations. If the number of people the student has evaluated is small, too friendly points are reduced from the total points. All the evaluation points from every evaluation the student has done are added to the too-friendly points, and an average is then calculated from that. This feature also needs a bigger database to give any proper information.<br><br><br><br>

<h2><a name="usability">USABILITY</a></h2>
Usability points taken into account while making the project:<br>
- The script run.sh to make the installation, building, and usage easier<br>
- The app uses an easy-to-use web interface. I have put effort into making the layout of the page intuitive and not overloaded.
- The page loads first and after that, you need to verify that you want to build the database since it takes a long time. The ability to select the timeframe from where the database is created has been added to allow the user to manage how much time is used to create the database. <br>
- A rough time estimate for database creation in the landing page to help with selecting the timeframe.<br>
- Paginated results for evaluations, separate page for each evaluation to give more information. This way the evaluations page is not too crowded.<br>
- The student page also shows all the evaluations done by the student so that they are easily accessible.
- Burbing unicorn to show that something actually happens and that the page is not just stuck loading data<br>
- Search option, where more search option can be added easily.<br>
- .csv download for evaluations in the selected time frame <br>
- Right hand navigator with easy access links to documentation.<br>
- I had planned to do early usability testing with two Hivers. They would have installed the app with the instructions given on the app's Github page while screen sharing and commenting on their experience when using it. Since I have quite limited experience in user experience and interface design, I would like to implement this test at some point to learn more about the things that other people find intuitive and easy to use.<br><br><br><br>

<h2><a name="database">DATABASE STRUCTURE:</a></h2>
tables:<br>
name, status, created, updated<br>
-> used to keep track if the database is ready. Reduces the amount of queries needed when developing.Can be later used to help with updating the database.<br><br>

projects:<br>
project_id, name, slug<br>
-> projects of cursus 42, in campus Helsinki. Used to cross reference scale_teams so that piscine evaluations are left out at this point.<br><br>

students:<br>
id, login, url, too_friendly_points, total<points, evals and avarage_points<br>
-> all the students of Hive Helsinki, used to collect the correct scale_teams from the database amd save student points.<br><br>

scales:<br>
corrector, total_points, id, scale_id, project_id, comment, comment_points, final_mark, final_mark_points, begin_at, corrected1, corrected2, corrected3, corrected4, too_friendly_points, filled_at, duration, duration_points, true_flags, flags_points, feedback_comment, feedback_rating, feedback_id, feedback_points, feedback_interested, feedback_nice, feedback_punctuality, feedback_rigorous, feedback_total_points, team_id<br>
-> selected info of evaluations<br><br><br><br>

<h2><a name="process">THE PROCESS OF MAKING THIS PROJECT</a></h2>
When I started the project I had never coded with python. I had some knowledge from the SQL day on PHP piscine on SQL but basically had to reinvent that too. I have evaluated the docker project of our courses a few times so I had a basic understanding of what Docker does, but working with it was new to me. Creating pages with python Bottle and templates was a new experience, but the knowledge I have on the front helped me with this a lot. <br>
I started the project by thinking about the points that in my opinion would give the most info about evaluations. I really wanted to integrate too friendly points and student average to the more obvious measures, since they would give so much more info and accuracy when trying to figure out if there is anything that would need bocal intervention.<br>
I started the technical process by figuring out how to request info from the 42 API. After some time I found the HiveHelsinki wrapper for API requests and integrated it into my project so that I could concentrate more on other things. I spend some time figuring out how to process the returned data and how python and its libraries work, and what libraries I would need to integrate into my project. From early on I decided to create the user interface with Bottle as a web page. When I was able to use the API enough to get the students at Hive Helsinki, I dockerized the project and started working on the database. I wanted to integrate the database early on since some of the ideas of calculating points required more data easily accessible. I also create the script to build and run docker and open the localhost page on the preferred browser early, thinking about the usability of the project.<br>
After that, I continued to develop the database hand in hand with the web page, so that the web page would give me a useful tool to access the data. After I created student listing and student pages I got stuck for a while trying to figure out a proper way to start the page before creating the database, and I also wanted to add some burbing unicorns to the time it took to build the database.<br>
After creating the evaluation listing I spend some with CSS creating a pretty and usable interface. I wanted to use the Hive colors and a font look-a-like to make the interface look like part of the Hive family. After I got the evaluation listing working with pagination, and a page for every evaluation with more information about the eval, I continued to make a search page so that a period of time can be accessed at a time. Up until this far, I had used my own evaluations only for the database, and after adding all of the evaluations I soon realized that it takes a lot of time and the hourly limit does no allow for a big database to be build from scratch, so I also added timeframe for database building on the starting page.<br>
The limits of the database creation that come from the hourly request limit and the time it takes to create the database make the app structure struggle since the idea behind it relies on a bigger database. It would work better hosted on a server, but I do not have that ability right now.<br><br><br><br>


<h2><a name="ideas">IDEAS FOR THE FUTURE:</a></h2>
- flag check<br>
- hosting on a server with a big database to allow bettering of the point calculation and student points.<br>
- more search options, like search evals by project, login or different points, or search students by login, project, etc.<br>
- database update possibility, the date and time when the database was created is saved.<br>
- possibility to sort searches and students/evals pages by different options, like certain points, correctors, correcteds, projects, etc. Also the amount of evals per page could be easily implemented.<br>
- check that search time is within database limits<br>
- add a rating of different areas (interested, nice, punctuality, rigorous)found on the feedback to eval page<br>
- secure connection<br>
- campus and cursus selection to database creation to allow portability to piscines and other campuses<br>
- progress bar for database creation<br>
- fine tuning the point system<br>
- export to .json<br>
- more work on the IU<br>
- discord notifications (discord stuff is something I have been eager to get to know, but have not had the time)<br>
- finetuning the too friendly points: also checking how many times the corrected has evaluated the corrector<br>
- checking the duration so that the actual duration of the evaluation is also saved and showed in the evaluation page<br>
- If evaluating a project the evaluator has not done them selves might be included somehow. If you have not done it, it
is really difficult to find more errors than others.<br>
- working together on a lot of projects and evaluating each other could be taken into account with too friendly points.<br>
+ notes after running a bigger test: cv project seems to give students the lowest points often. Might need some balancing?<br><br><br><br>

<h2><a name="other">OTHER INFO:</a></h2>
Unicorn burb by Mauro Gatti on Dribbble<br>
The basic html structure and css from W3Schools<br>
src/intra.py 42API wrapper from Hive Helsinki Github<br><br><br><br>

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