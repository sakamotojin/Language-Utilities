const JSSoup = require('jssoup').default;

var soup = new JSSoup('<html><head>hello</head></html>');
var tag = soup.find('head');
// tag.name
// // 'head'
// tag.name = 'span'
console.log(tag)
//<span>hello</span>