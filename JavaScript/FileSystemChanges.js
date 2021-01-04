const Fs = require('fs')

function lastUpdatedDate (file) {  
  const { mtime, ctime } = Fs.statSync(file)

  console.log(`File data   last modified: ${mtime}`)
  console.log(`File status last modified: ${ctime}`)

  return mtime
}

lastUpdatedDate('./file.txt')  