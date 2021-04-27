sudo docker image rm -f eval
sudo docker build -t eval .
if test ! -f "config.yml"; then
	mv config_example.yml config.yml
fi
xdg-open "http://localhost:6660/"
sudo docker run -p 6660:6660 -t -i eval
