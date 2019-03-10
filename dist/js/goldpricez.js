

function goldpull(){
  var xhttp=new XMLHTTPRequest();
  xhttp.onreadystatechange=function(){
    var response=JSON.parse(xhttp.responseText);
    var oldusgold=response['T1']['ound_price_usd'];
    var newusgold=response['T']['ound_price_usd'];
    var goldchange=(newusgold-oldusgold)/oldusgold;
    var oldspxtogold=response['T1']['spx/gold'];
    var newspxtogold=response['T']['spx/gold'];
    var spxtogoldchange=(newspxtogold-oldspxtogold)/oldspxtogold;
    var output='<tr>'+
    '<td>Gold Price USD</td>'+
    '<td>'+newusgold+'</td>'+
    '<td>Gold Price Change:'+'</td>'+
    '<td>'+goldchange+'</td>'+
    '<td>SPX to Gold Ratio</td>'+
    '<td>'+newspxtogold+'</td>'+
    '<td>SPX to Gold Ratio Change %:</td>'+
    '<td>'+spxtogoldchange+'</td>'+
    '</tr>';
    document.getElementById('goldtable').innerHTML=output;
    xhttp.open("Get","/json/goldpricez.json",true);
    xhttp.send();

  }


}