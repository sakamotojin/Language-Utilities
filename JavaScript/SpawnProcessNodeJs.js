const { spawn } = require('child_process');
const ls = spawn('start',['firefox.exe' ,'aitpune.com'],{stdio: 'inherit', shell: true});

// ls.stdout.on('data', (data) => {
// 	console.log('data');
//   //console.log(`stdout: ${data}`);
// });

// ls.stderr.on('data', (data) => {
// 	console.log('dataerror');
//  // console.error(`stderr: ${data}`);
// });

ls.on('close', (code) => {
	console.log('close');
  console.log(`child process exited with code ${code}`);
});