<!DOCTYPE html>
<html>
<body>

<h2>The unicorns are burbing the database to life!</h2>
%
<img src="images/{{picture}}">
%end

<p>You will be redirected once the database is ready. In the meanwhile, take a look at the <a href="documentation.html" target="_blank">documentation!</a></p>

<script>
window.post = function(url, data) {
  return fetch(url, {method: "POST", body: JSON.stringify(data)});
}

window.addEventListener('load', (event) => {
  post("wait.html", {start: 1});
});

</script>
</body>
</html>