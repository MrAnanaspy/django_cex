const json = json1;
let test = JSON.parse(json);
const data = JSON.parse(json);
data.sort((a, b) => a.name2 > b.name2 ? -1 : 1);
const table = $('<table class = "table"></table>');
const tbody = $('<tbody></tbody>');


function addAllColumnHeaders(data) {
  const columnSet = new Set();
  data.forEach(item => Object.keys(item).forEach(key => columnSet.add(key)));
  const tr = $('<tr></tr>');
  const thead = $('<thead></thead>');
  columnSet.forEach(header => tr.append($('<th></th>').text(header)));
  thead.append(tr)
  table.append(thead);
}

addAllColumnHeaders(data);


data.forEach(item => {
  const tr = $('<tr></tr>');
  Object.values(item).forEach(value => tr.append($('<td></td>').text(value)));
  tbody.append(tr);
});
table.append(tbody)
$('body').append(table);
$('head').append('<link rel="stylesheet" href="css.css">');




data.sort((a, b) => a.name2 > b.name2 ? -1 : 1);

console.log(typeof(data))