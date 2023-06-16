document.addEventListener("DOMContentLoaded", function(event) {
    sub_found    = document.getElementById("headSubdomainsFound");
    tak_found    = document.getElementById("headTakeoversFound");
    scn_domains  = document.getElementById("headScannedDomains");
    sessions     = document.getElementById("headSessions");
    progressbar  = document.getElementById("progressBar");
    appendsection = document.getElementById("appendSection");

    refresh();
    setInterval(function(){
        refresh();
    }, 10000);
    // Send a 'init' message.  This tells integration tests that we are ready to go
    cockpit.transport.wait(function() { });
});

function formatStringToList(str) {
    // Split the string into words
    const words = str.split(' ');
    return words.map(word => `${word}`);
}

function get_all_subs(){
    let comm = "get_all_subs"
    comm     = formatStringToList(comm);
    cockpit.spawn(comm)
    .stream(function(data) {
        // split in javascript
        sub_found.innerHTML = data;
    })
    .then(function(){

    })
    .catch(function(error, data) {
        console.log("GET_SUBDOMAINS ERROR: " + data);
    });
}

function get_all_takeovers(){
    let comm = "get_all_takeovers"
    comm     = formatStringToList(comm);
    cockpit.spawn(comm)
    .stream(function(data) {
        // split in javascript
        tak_found.innerHTML = data;
    })
    .then(function(){

    })
    .catch(function(error, data) {
        console.log("GET_TAKEOVER ERROR: " + data);
    });
}

function get_all_domains(){
    let comm = "get_all_domains"
    comm     = formatStringToList(comm);
    cockpit.spawn(comm)
    .stream(function(data) {
        // split in javascript
        scn_domains.innerHTML = data;
    })
    .then(function(){

    })
    .catch(function(error, data) {
        console.log("GET_DOMAINS ERROR: " + data);
    });
}

function get_active_sessions(){
    let comm = "get_active_sessions"
    comm     = formatStringToList(comm);
    cockpit.spawn(comm)
    .stream(function(data) {
        // split in javascript
        sessions.innerHTML = data;
    })
    .then(function(){

    })
    .catch(function(error, data) {
        console.log("GET_SESSIONS ERROR: " + data);
    });
}

function get_tables(){
    let comm = "get_tables"
    comm     = formatStringToList(comm);
    cockpit.spawn(comm)
    .stream(function(data) {
        // split in javascript
        console.log("Table data: " + data);
        const jsonObject = JSON.parse(data);
        
        appendsection.innerHTML = "";
        for (let key in jsonObject){
            if(jsonObject.hasOwnProperty(key)){
                let _arr = jsonObject[key];
                toappend = '<tr style="font-size: 20px !important;">' +
                '<td style="font-weight:lighter;">' + _arr[2].replace('_', ' ') + '</td>' +
                '<td style="color: #8a7f0e">' + _arr[1] + '</td>' +
                '<td style="color: #000">' + key + '</td>' +
                '<td class="text-right"><span class="'+ (parseInt(_arr[0], 10) != 0 ? 'red-bolder' : 'green-bolder') +'">' + _arr[0] + '</span></td>' +
                '<td class="text-right"><span class="green-bolder">' + _arr[3] + '</span></td>' +
                '<td class="text-right">' +
                    '<button title="Download" '+ (_arr[3] != "Completed" ? "disabled" : '') +' type="button" class="btn btn-success" onClick="downloadFile(\'/cockpit/static/subtakes/'+ key +'/report.csv\', \''+ key +'.csv\')">' +
                        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">' +
                            '<path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>' +
                            '<path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>' +
                        '</svg>' +
                    '</button>' +
                    '<button title="Stop" '+ (_arr[3] == "Completed" || _arr[3] == "Killed" ? "disabled" : '') +' type="button" class="btn btn-danger" onClick="killSession(\''+ key +'\')">' +
                        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-stop" viewBox="0 0 16 16">' +
                            '<path d="M3.5 5A1.5 1.5 0 0 1 5 3.5h6A1.5 1.5 0 0 1 12.5 5v6a1.5 1.5 0 0 1-1.5 1.5H5A1.5 1.5 0 0 1 3.5 11V5zM5 4.5a.5.5 0 0 0-.5.5v6a.5.5 0 0 0 .5.5h6a.5.5 0 0 0 .5-.5V5a.5.5 0 0 0-.5-.5H5z"/>' +
                        '</svg>' +
                    '</button>' +
                    '<button title="Delete" '+ (_arr[3] == "Completed" || _arr[3] == "Killed" ? "" : 'disabled') +' type="button" class="btn btn-warning" onClick="deleteScan(\'' + key + '\')">' +
                        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">' +
                            '<path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5ZM11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H2.506a.58.58 0 0 0-.01 0H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1h-.995a.59.59 0 0 0-.01 0H11Zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5h9.916Zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47ZM8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5Z"/>' +
                        '</svg>' +
                    '</button>' +
                '</td>' +
                '</tr>'

                appendsection.innerHTML += toappend;
            }
        }
    })
    .then(function(){
        progressbar.style.display = "none";
    })
    .catch(function(error, data) {
        console.log("GET_TABLES ERROR: " + data);
        progressbar.style.display = "none";
    });
}

function refresh(){
    get_all_subs()
    get_all_takeovers()
    get_all_domains()
    get_active_sessions()
    get_tables()
}

function downloadFile(url, fileName) {
    // Create an anchor element
    console.log("Downloading: " + url);
    const link = document.createElement('a');
    link.href = url;
    link.download = fileName;
  
    // Append the link to the body
    document.body.appendChild(link);
  
    // Trigger the click event
    link.click();
  
    // Clean up
    document.body.removeChild(link);
}

function deleteScan(domain){
    let comm = "rm -rf /usr/share/cockpit/static/subtakes/" + domain;
    comm     = formatStringToList(comm);
    progressbar.style.display = "block";
    cockpit.spawn(comm)
    .stream(function(data) {
        refresh();
    })
    .then(function(){
    })
    .catch(function(error, data) {
        console.log("Delete Domain Error: " + error);
    });
}

function killSession(domain){
    let sessionname = domain.replace(/\./g, "");
    let comm = "tmux kill-session -t " + sessionname;
    comm     = formatStringToList(comm);
    progressbar.style.display = "block";
    cockpit.spawn(comm)
    .stream(function(data) {
        refresh();
    })
    .then(function(){
    })
    .catch(function(error, data) {
        console.log("Kill Session Error: " + error);
    });
}