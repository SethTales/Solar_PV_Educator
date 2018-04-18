
//request params for asynchronous call to NREL Solar Incentives api to gather data about different types of incentives and rebates available
//to people who are evaluating purchasing solar electricity
function setRequestParameters()
{
    var apiKey = "rH3Vxikvbxm5SnbW3Lxgs3c76L4hjbXph0NoQlzw";
    var address = document.getElementById("zip").value;
    var category = "solar_technologies";
    var technology = "solar_photovoltaics";
    console.log("setRequestParams Called");
    return("https://developer.nrel.gov/api/energy_incentives/v2/dsire.json?API_KEY=" + apiKey + "&address=" + address + "&category=" + category + "&technology=" + technology);
}

function sendApiRequest()
{
    var requestUrl = setRequestParameters();
    var request = new XMLHttpRequest();
    
    request.onreadystatechange = function ()
    {
        if(request.readyState == 4 && request.status == 200)
        {
            getRequestCallback(request.responseText);
            document.getElementById("loader").style.display = 'none';
            document.getElementById("incentivesTable").style.display = 'contents';
        }
    };

    request.open("GET", requestUrl, true);
    request.send();
    console.log(requestUrl);
}

function getRequestCallback(response)
{
    var jsonResponse = JSON.parse(response);
    populateIncentivesTable(jsonResponse);

}

function populateIncentivesTable(jsonResponse)
{
    var table = document.getElementById("incentivesTable");

    //add rows equal to the count of incentives returned by the Energy Incentives API response
    //starts with i+1 because table header is statically generated

    for(var i = 0; i < jsonResponse.metadata.resultset.count; i++)
    {
        var category = jsonResponse.result[i].category_name;
        var name = jsonResponse.result[i].program_name;
        var url = jsonResponse.result[i].public_url;
        var type = jsonResponse.result[i].regions[0].name;

        var row = table.insertRow(1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);

        cell1.innerHTML = category;
        cell2.innerHTML = name;
        cell3.innerHTML = "<a href=" + url + ">" + url + "</a>";
        cell4.innerHTML = type;
    }
}