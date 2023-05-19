
reddvid () {
    wget https://reddvid.herokuapp.com/$(curl -X GET 'https://reddvid.herokuapp.com/' --form "url=\"${1}\"}" | jq -r '.download')
}

