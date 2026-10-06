fetch(url, { headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })

function token() { return localStorage.getItem("token"); }

console.log(token())