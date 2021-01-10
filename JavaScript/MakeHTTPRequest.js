const https = require('https');
const jssoup = require('jssoup').default;

// var options = {
//     host: 'www.imdb.com',
//     port: 443,
//     path: '/chart/top/',
//     method: 'GET'
// };
// var req = https.request(options, function (res) {


var data = "";

var req = https.get('https://www.imdb.com/chart/top/', function (res) {
    
    res.setEncoding('utf8');
    res.on('data', function (chunk) {
        data += chunk;
    });

    res.on('end', () => {
        console.log('end the connections');
        parse_html(data);
    });
});


req.on('error' , (err)=>{
    console.log(err.message);
});

setTimeout(()=>{
    console.log('over');
},3000);


function parse_html(data){
    
    let soup = new jssoup(data);
    let movie_data = soup.findAll('tbody','lister-list');
    

};

