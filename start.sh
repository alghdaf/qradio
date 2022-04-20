echo "Cloning Repo...."
if [ -z $BRANCH ]
then
  echo "Cloning main branch...."
  git clone https://github.com/alghdaf/qradio /qradio
else
  echo "Cloning $BRANCH branch...."
  git clone https://github.com/alghdaf/qradio -b $BRANCH /qradio
fi
cd /qradio
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 main.py
