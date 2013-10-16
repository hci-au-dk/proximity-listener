sudo airmon-ng
rm -f proximity-01.csv
sudo airodump-ng mon0 --output-format csv -w proximity
