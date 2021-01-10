const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const https = require('https');
//const { table } = require("console");


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


req.on('error', (err) => {
    console.log(err.message);
});

setTimeout(() => {
    console.log('over');
}, 3000);


var movie_list = [];
function parse_html(data) {

    let rank = 0 ;
    let document = new JSDOM(String(data)).window.document;
    let movie_table = Array.from(document.getElementsByTagName('tr'));
   // console.log(movie_table);
    movie_table.forEach((ele,err) => {

        let movie_info = {};
        Array.from(ele.cells).forEach((cell, err) => {
            if(rank > 0){
                if (cell.matches('.titleColumn')){
                    movie_info["rank"] = rank;
                    movie_info["name"] = cell.children[0].textContent;
                    movie_info["year"] = cell.children[1].textContent;
                    let people = cell.children[0].getAttribute("title").split(',');
                    movie_info["people"] = people;
                    //console.log(cell.children[0].textContent + " " + cell.children[1].textContent + " " + cell.children[0].getAttribute("title"));
                
                }
                if (cell.matches('.imdbRating')) {
                    //console.log(cell.children[0].textContent);
                    movie_info["rating"] = cell.children[0].textContent;
                }

            }
        });
        rank = rank +1;
        movie_list.push(movie_info);
    });

    movie_list.forEach((ele,err)=>{
        console.log(ele);
    });
};



