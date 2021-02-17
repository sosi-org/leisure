const fs = require('fs');
//const fetch = require('fetch');
// npm install superagent@6.1.0
const superagent = require('superagent');

const {token} = JSON.parse(fs.readFileSync('./secrets.json'));
const config = {
  botname: 'sosifetch1bot',
  boturl: 't.me/sosifetch1bot',
  ...{token},
};

console.log(config);

/*
// const a = fetch(`https://api.telegram.org/bot${token}`);
const a = fetch(`https://yahoo.com`);
console.log(a);
*/


superagent.get(`https://api.telegram.org/bot${token}/GET`)
.query({ api_key: 'DEMO_KEY', date: '2017-08-02' })
.end((err, res) => {
  if (err) { return console.log(err); }
  //console.log(res.body.url);
  //console.log(res.body.explanation);
  console.log(res.body);
});
