# echo "generating requirement.txt"
# cd qi-server || exit
# pipreqs ./ --force

# cd ..
echo "building frontend"
cd qi-frontend || exit
yarn build

echo "building docker image"
cd .. || exit
docker build -t qi .
