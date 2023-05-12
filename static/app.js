
async function loadCupcakes() 
{
    const cupcakes = await retrieveCupcakes();
    generate_list_nodes(cupcakes);
}

async function retrieveCupcakes()
{
    const res = await axios.get(`/api/cupcakes`);
    console.log(res.data['cupcakes']);
    cupcakes = res.data['cupcakes'];
    return cupcakes
}

function generate_list_nodes(list)
{
    let html_list = [];
    for(cupcake of list)
    {
        const listItem = document.createElement('li');
        listItem.innerHTML = `<h3>Flavor: ${cupcake['flavor']} - Rating: ${cupcake['rating']}</h3>`;
        listItem.id = `${cupcake['id']}`;
        $('#cupcake_list').append(listItem);
    }
    return $('#cupcake_list');
}

$(document).ready(loadCupcakes);

async function postCupcakes(evt)
{
    evt.preventDefault();

    flavor = $("#flavor").val()
    size = $("#size").val()
    rating = $("#rating").val()
    image = $("#image").val()

    res = await axios.post('/api/cupcakes', {flavor: flavor, size: size, rating: rating, image: image});
    $("#cupcake_list").empty();
    await loadCupcakes();
}

$("#add-form").on('submit', postCupcakes)
