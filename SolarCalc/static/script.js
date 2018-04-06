
function validateZip()
{
    var zipRegEx = /^\d{5}$/;
    var zip = document.getElementById('zip').value;
    var found = zipRegEx.test(zip);
    console.log(zip);

    if(found == true)
    {
        console.log(found);
        var zipError = document.getElementById('zipCodeError').style.display = 'none';
        var zipInput = document.getElementById('zip').style.border = '2px solid green';
        return(true);
        
    }
    else
    {
        console.log(found);
        var zipError = document.getElementById('zipCodeError').style.display = 'contents';
        var zipInput = document.getElementById('zip').style.border = '2px solid red';
        return(false);
    }
}

function validateCostPerKwh()
{
    var elecCostRegex = /^[0]?(\.[1-9]+){1}[0-9]{0,2}|^[0]?(\.[0-9]{1}){1}[1-9]{1}[0-9]?/;
    var elecCost = document.getElementById('costPerKwh').value;
    var found = elecCostRegex.test(elecCost);

    if(found == true)
    {
        console.log(found);
        var zipError = document.getElementById('costPerKwhError').style.display = 'none';
        var zipInput = document.getElementById('costPerKwh').style.border = '2px solid green';
        return(true);
        
    }
    else
    {
        console.log(found);
        var zipError = document.getElementById('costPerKwhError').style.display = 'contents';
        var zipInput = document.getElementById('costPerKwh').style.border = '2px solid red';
        return(false);
    }
}

function validateSysCap()
{
    var sysCap = document.getElementById('sys_cap').value;

    if(isNaN(sysCap))
    {
        console.log(false);
        var sys_capError = document.getElementById('sys_capError').style.display = 'contents';
        var sys_capError = document.getElementById('sys_cap').style.border = '2px solid red';
        return(false);
        
    }
    else if(sysCap < 0.05)
    {
        console.log(false);
        var sys_capError = document.getElementById('sys_capError').style.display = 'contents';
        var sys_capError = document.getElementById('sys_cap').style.border = '2px solid red';
        return(false);
    }
    else if(sysCap > 500000)
    {
        console.log(false);
        var sys_capError = document.getElementById('sys_capError').style.display = 'contents';
        var sys_capError = document.getElementById('sys_cap').style.border = '2px solid red';
        return(false);
    }
    else
    {
        console.log(true);
        var sys_capError = document.getElementById('sys_capError').style.display = 'none';
        var sys_capError = document.getElementById('sys_cap').style.border = '2px solid green';
        return(true);
    }
}

function validateTilt()
{
    var tilt = document.getElementById('tilt').value;

    if(isNaN(tilt))
    {
        console.log(false);
        var sys_capError = document.getElementById('tiltError').style.display = 'contents';
        var sys_capError = document.getElementById('tilt').style.border = '2px solid red';
        return(false);
        
    }
    else if(tilt <= 0)
    {
        console.log(false);
        var sys_capError = document.getElementById('tiltError').style.display = 'contents';
        var sys_capError = document.getElementById('tilt').style.border = '2px solid red';
        return(false);
    }
    else if(tilt > 90)
    {
        console.log(false);
        var sys_capError = document.getElementById('tiltError').style.display = 'contents';
        var sys_capError = document.getElementById('tilt').style.border = '2px solid red';
        return(false);
    }
    else
    {
        console.log(true);
        var sys_capError = document.getElementById('tiltError').style.display = 'none';
        var sys_capError = document.getElementById('tilt').style.border = '2px solid green';
        return(true);
    }
}

function validateAzimuth()
{
    var azimuth = document.getElementById('azimuth').value;

    if(isNaN(azimuth))
    {
        console.log(false);
        var sys_capError = document.getElementById('azimuthError').style.display = 'contents';
        var sys_capError = document.getElementById('azimuth').style.border = '2px solid red';
        return(false);
    }
    else if(azimuth < 0)
    {
        console.log(false);
        var sys_capError = document.getElementById('azimuthError').style.display = 'contents';
        var sys_capError = document.getElementById('azimuth').style.border = '2px solid red';
        return(false);
    }
    else if(azimuth > 359.9)
    {
        console.log(false);
        var sys_capError = document.getElementById('azimuthError').style.display = 'contents';
        var sys_capError = document.getElementById('azimuth').style.border = '2px solid red';
        return(false);
    }
    else
    {
        console.log(true);
        var sys_capError = document.getElementById('azimuthError').style.display = 'none';
        var sys_capError = document.getElementById('azimuth').style.border = '2px solid green';
        return(true);
    }
}

function validateLosses()
{
    var losses = document.getElementById('losses').value;

    if(isNaN(losses))
    {
        console.log(false);
        var sys_capError = document.getElementById('lossesError').style.display = 'contents';
        var sys_capError = document.getElementById('losses').style.border = '2px solid red';
        return(false);
        
    }
    else if(losses < 0)
    {
        console.log(false);
        var sys_capError = document.getElementById('lossesError').style.display = 'contents';
        var sys_capError = document.getElementById('losses').style.border = '2px solid red';
        return(false);
    }
    else if(losses > 99)
    {
        console.log(false);
        var sys_capError = document.getElementById('lossesError').style.display = 'contents';
        var sys_capError = document.getElementById('losses').style.border = '2px solid red';
        return(false);
    }
    else
    {
        console.log(true);
        var sys_capError = document.getElementById('lossesError').style.display = 'none';
        var sys_capError = document.getElementById('losses').style.border = '2px solid green';
        return(true);
    }
}

function validateForm()
{
    var bool = validateZip();
    if (bool == false)
    {
        alert("One or more of your inputs is incorrect. Please check then re-submit.")
        return(false);
    }
    bool = validateCostPerKwh()
    if (bool == false)
    {
        alert("One or more of your inputs is incorrect. Please check then re-submit.")
        return(false);
    }
    bool = validateSysCap()
    if (bool == false)
    {
        alert("One or more of your inputs is incorrect. Please check then re-submit.")
        return(false);
    }
    bool = validateTilt()
    if (bool == false)
    {
        alert("One or more of your inputs is incorrect. Please check then re-submit.")
        return(false);
    }
    bool = validateAzimuth()
    if (bool == false)
    {
        alert("One or more of your inputs is incorrect. Please check then re-submit.")
        return(false);
    }
    bool = validateLosses()
    if (bool == false)
    {
        alert("One or more of your inputs is incorrect. Please check then re-submit.")
        return(false);
    }
    else
    {
        return(true);
    }
}

function preventFormSubmit()
{
    document.getElementById('submit').addEventListener('click', function(event){
        event.preventDefault();
    });
}