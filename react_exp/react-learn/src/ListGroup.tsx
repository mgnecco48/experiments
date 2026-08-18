function handleClick() {
    alert('Salsas ordered!');
}

function listGroup() {
    return (
        <ul className='m-4 p-4 bg-white rounded shadow'>
            <li>Salsa Verde</li>
            <li>Salsa Roja</li>
            <li>Salsa Tatemada</li>
            <li>Salsa Habanero</li>
            <button
                onClick={handleClick}
                className='mt-4 bg-red-600 px-4 py-2 text-white hover:bg-red-300'>
                Order Salsas
            </button>

        </ul>
    );


}

export default listGroup;   
