google.charts.load('current', {'packages':['corechart']});
google.charts.load('current', {'packages':['table']});


var autoReload;
var hostInfo,memoryInfo,diskInfo,cpuInfo,idHote = null;

function refreshDatas(){
  autoreload = null;
  idHote = this.document.getElementById('selectedMachine').value;
  setupDatas();
  if(idHote != undefined){
    displayHostInfo();
    drawMemoryInfo();
    drawCPUInfo();
    drawDiskInfo();
  }
}

function setupDatas(){
  if( autoReload == null){
    autoReload = setInterval(refreshDatas,1500);
  }
  fetch('/machine/'+idHote+'/hostInfo')
	.then(response => response.json())
	.then(data => {
    this.hostInfo = data;
	})
  .catch(error => console.error(error));
  fetch('/machine/'+idHote+'/getMemoryInfo')
	.then(response => response.json())
	.then(data => {
    this.memoryInfo = data;
	})
  .catch(error => console.error(error));
  fetch('/machine/'+idHote+'/getCPUInfo')
	.then(response => response.json())
	.then(data => {
    this.cpuInfo = data;
	})
  .catch(error => console.error(error));
  fetch('/machine/'+idHote+'/getDiskInfo')
	.then(response => response.json())
	.then(data => {
    this.diskInfo = data;
	})
  .catch(error => console.error(error));
}
function displayHostInfo(){
  document.getElementById('hostName').innerHTML = "<h6>Nom de la machine : </h6>"+ hostInfo.nom
  document.getElementById('operatingSystem').innerHTML = "<h6>Système d'exploitation : </h6>"+ hostInfo.OS
  document.getElementById('kernel').innerHTML = "<h6>Noyau : </h6>"+ hostInfo.noyaux
  document.getElementById('uptime').innerHTML = "<h6>Uptime : </h6>"+ hostInfo.uptime
}
function drawMemoryInfo() {
  var dataTable = new google.visualization.DataTable();
  dataTable.addColumn('number', 'Total');
  dataTable.addColumn('number', 'Free');
  dataTable.addColumn('number', 'Used');
  dataTable.addColumn('number', 'Buffers');
  dataTable.addColumn('number', 'Cached');

  for(var i = 0; i < memoryInfo.memoryUsage.length; i++){
    dataTable.addRow([memoryInfo.memoryUsage[i].memoireTotal/1024/1024,
      memoryInfo.memoryUsage[i].memoireLibre/1024/1024,
      memoryInfo.memoryUsage[i].memoireOccupe/1024/1024,
      memoryInfo.memoryUsage[i].buffer/1024/1024,
      memoryInfo.memoryUsage[i].cache/1024/1024]);
  }

  var options_stacked = {
    title: 'Utilisation Mémoire',
    isStacked: 'relative',
    height: 300,  
    legend: {maxLines: 3},
    vAxis: {
      minValue: 0,
      ticks: [0,.15, .3, .45, .6, .75,.9, 1]
    }
  };

  var chart = new google.visualization.AreaChart(document.getElementById('memoryInfo'));
  chart.draw(dataTable, options_stacked);
}
function drawCPUInfo() {
  var cpuUsed = 0;
  var freeCPU = 0;
  var dataTable = new google.visualization.DataTable();
  dataTable.addColumn('string', 'CPU');
  dataTable.addColumn('number', 'Used');
  for(var index = 0; index < cpuInfo.cpuUsage.length; index++) { 
    freeCPU = freeCPU + cpuInfo.cpuUsage[index].frequenceMax;
    cpuUsed = cpuUsed + cpuInfo.cpuUsage[index].frequence;
  }
  freeCPU = freeCPU / cpuInfo.cpuUsage.length;
  cpuUsed = cpuUsed / cpuInfo.cpuUsage.length;
  dataTable.addRow(["CPU Utilisé",cpuUsed]);
  dataTable.addRow(["CPU Disponible",freeCPU]);

  var options = {
    title: 'Utilisation CPU',
    pieHole: 0.4,
  };

  var chart = new google.visualization.PieChart(document.getElementById('cpuInfo'));
  chart.draw(dataTable, options);
}


function drawDiskInfo() {
  var dataTable = new google.visualization.DataTable();
  dataTable.addColumn('string', 'Available');
  dataTable.addColumn('string', 'File system');
  dataTable.addColumn('string', 'Mounted');
  dataTable.addColumn('string', 'Pourcentage');
  dataTable.addColumn('string', 'Size');
  dataTable.addColumn('string', 'Used');
  for(var i = 0; i < diskInfo.diskUsage.length; i++){
    dataTable.addRow([readableBytes(diskInfo.diskUsage[i].available),
      diskInfo.diskUsage[i].fileSystem,
      diskInfo.diskUsage[i].mounted,
      diskInfo.diskUsage[i].pourcentage,
      readableBytes(diskInfo.diskUsage[i].size),
      readableBytes(diskInfo.diskUsage[i].used)]);
  }
  var table = new google.visualization.Table(document.getElementById('diskInfo'));
  table.draw(dataTable, {width: '100%', height: '100%'});
}
function readableBytes(bytes) {
  var i = Math.floor(Math.log(bytes) / Math.log(1024)),
  sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

  return (bytes / Math.pow(1024, i)).toFixed(2) * 1 + ' ' + sizes[i];
}

