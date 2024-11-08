// const { client_encoding } = require("pg/lib/defaults");

const searchbar = document.querySelector('#search');
const suggestions = document.querySelector('.suggestions ul');
const mapDiv = document.querySelector('#map');
const stationInfo = document.querySelector('#stationInfo');
const addButton = document.querySelector('#addButton');
// let cities = JSON.parse(document.querySelector('#citylist').getAttribute('name'))


searchbar.addEventListener('keyup', searchHandler);
suggestions.addEventListener('click', useSuggestion);
mapDiv.addEventListener('click', showStation);



function search(str) {
    // console.log(str);
	let results = [];

	results = networks.filter(n => n.location.city.toLowerCase().includes(str));

	return results;
}

function searchHandler(e) {
	suggestions.innerHTML="";
	if (searchbar.value && searchbar.value.length >= 2){
        // console.log(search(searchbar.value.toLowerCase()));
		showSuggestions(search(searchbar.value.toLowerCase()));
	}
}

function showSuggestions(results, inputVal) {

	for (let n in results){
		const listItem = document.createElement("li");
        let r = results[n];
        listItem.setAttribute("id", r.id);
		listItem.innerHTML=("<b>" + r.location.city + "</b>" + ", " + r.name);
		suggestions.appendChild(listItem);
	}
}

function useSuggestion(e) {
    let id = e.target.closest('li').id;
	suggestions.innerHTML="";
    window.location.href = '/' + id;
}

function showStation(e) {
	let stationId = e.target.closest('div').id;
	station = network["stations"].find(n => n.id == stationId);
	networkId = network["id"];
	stationInfo.innerHTML = `
	<div class="station-text">
	<p>Address: ${ station.name }</p>
    <p>Free bikes: ${ station.free_bikes }    Empty slots: ${ station.empty_slots }</p>
	</div>
	<form>
	<button type = submit id="addButton" formaction= "/${networkId}/${stationId}"> Add station to favourites </button>
	</form>
	`
}


