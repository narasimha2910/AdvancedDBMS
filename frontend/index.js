async function test() {
  var season = document.getElementById("season");
  var location = document.getElementById("location");
  var tb = document.getElementById("tablebody");
  tb.innerHTML=""
  var obj = {};
  if (location.value) obj["location"] = location.value;
  if (season.value) obj["season"] = season.value;
  var response = await fetch("http://127.0.0.1:5001/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(obj),
  }).then((res) => res.json());
  console.log(response);
  response.crop_list.forEach(function (c) {
    var tr = document.createElement("tr");
    tr.innerHTML = `<th scope="row">${c.f.name}</th>
              <td>${c.c.name}</td>
              <td>${c.c.location}</td>
              <td>${c.c.net_yield}</td>
              <td>${c.c.season}</td>`;
    tb.append(tr);
  });
  season.value = "";
  location.value = "";
}
