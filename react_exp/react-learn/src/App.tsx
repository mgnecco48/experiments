import { useEffect, useState } from 'react';

type Salsa = {
    item_name: string
    spice_level: string
    image_url: string
    size: number
    price: number
};

type OrderItem = Salsa & {
    quantity: number
};



function App() {

    const [salsaList, setSalsaList] = useState<Salsa[]>([]);
    const [cartQuantities, setCartQuantities] = useState<Record<string, number>>({});
    const [orderItems, setOrderItems] = useState<OrderItem[]>([]);

    useEffect(() => {
        async function fetchSalsas() {
            const response = await fetch('http://127.0.0.1:8000/salsas/');
            const data = await response.json();
            setSalsaList(data);
        }
        fetchSalsas();
    }, []);

    function increaseQuantity(itemName: string) {
        setCartQuantities((currentQuantities) => ({
            ...currentQuantities,
            [itemName]: (currentQuantities[itemName] || 0) + 1,
        }));
    }

    function decreaseQuantity(itemName: string) {
        setCartQuantities((currentQuantities) => ({
            ...currentQuantities,
            [itemName]: Math.max((currentQuantities[itemName] || 0) - 1, 0),
        }));
    }

    function handleClick() {
        const selectedSalsas = salsaList
            .map((salsa) => ({
                ...salsa,
                quantity: cartQuantities[salsa.item_name] || 0,
            }))
            .filter((salsa) => salsa.quantity > 0);

        if (selectedSalsas.length === 0) {
            alert('Your cart is empty');
            return;
        }

        console.log('Ordered salsas:', selectedSalsas);
        setOrderItems(selectedSalsas);
        setCartQuantities({});
    }

    const totalItems = salsaList.reduce(
        (total, salsa) => total + (cartQuantities[salsa.item_name] || 0),
        0
    );
    const totalPrice = salsaList.reduce(
        (total, salsa) =>
            total + (cartQuantities[salsa.item_name] || 0) * salsa.price,
        0
    );

    if (orderItems.length > 0) {
        return (
            <OrderOverview
                orderItems={orderItems}
                onBack={() => setOrderItems([])}
            />
        );
    }


    return (
        <div className="font-roboto min-h-screen bg-[#f5f0e6] px-4 py-6 sm:px-8 lg:px-12">
            <div className="fixed right-3 top-3 z-50 sm:right-6 sm:top-6">
                <CartTotal totalItems={totalItems} totalPrice={totalPrice} />
            </div>

            <PageHeader />

            <section className="mx-auto mt-10 max-w-7xl rounded-3xl bg-red-100 px-4 py-8 shadow-sm sm:px-6 lg:px-8">
                <h2 className="text-3xl font-bold tracking-tight text-gray-900">Salsas</h2>

                <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                    {salsaList.map((salsa) => {
                        const amount = cartQuantities[salsa.item_name] || 0;

                        return (
                            <div key={salsa.item_name} className="rounded-2xl bg-white p-3 shadow-sm transition hover:-translate-y-1 hover:shadow-md">
                                <img
                                    alt={salsa.item_name}
                                    src={salsa.image_url}
                                    className="aspect-square w-full rounded-xl bg-gray-200 object-cover"
                                />
                                <div className="mt-4 flex justify-between gap-4">
                                    <div>
                                        <h3 className="text-base font-semibold text-gray-900">
                                            <a href={salsa.item_name}>
                                                {salsa.item_name}
                                            </a>
                                        </h3>
                                        <p className="mt-1 text-base text-gray-500">{salsa.spice_level}</p>
                                    </div>
                                    <p className="shrink-0 text-base font-medium text-gray-900">{salsa.price} NOK</p>
                                </div>
                                <CardCounter
                                    amount={amount}
                                    onDecrease={() => decreaseQuantity(salsa.item_name)}
                                    onIncrease={() => increaseQuantity(salsa.item_name)}
                                />
                            </div>
                        );
                    })}
                </div>

                <button
                    onClick={handleClick}
                    className="mt-8 w-full rounded-xl bg-red-600 py-4 text-xl font-semibold text-white hover:bg-red-700"
                >
                    Order salsas
                </button>
            </section>
        </div>

    );
}

function PageHeader() {
    return (
        <header className="mx-auto max-w-7xl pt-16 text-center sm:pt-8">
            <h1 className="font-pirata text-6xl font-bold leading-tight text-red-600 sm:text-6xl lg:text-9xl">
                Condimentos Superior
            </h1>
            <p className="mt-4 text-base text-gray-500 sm:text-lg">
                Ricas Salsas hechas a mano.
            </p>
        </header>
    );
}

function OrderOverview({
    orderItems,
    onBack,
}: {
    orderItems: OrderItem[];
    onBack: () => void;
}) {
    const totalItems = orderItems.reduce(
        (total, item) => total + item.quantity,
        0
    );
    const totalPrice = orderItems.reduce(
        (total, item) => total + item.quantity * item.price,
        0
    );

    return (
        <div className="font-roboto min-h-screen bg-[#f5f0e6] px-4 py-6 sm:px-8 lg:px-12">
            <PageHeader />

            <main className="mx-auto mt-10 max-w-7xl rounded-3xl bg-red-100 px-4 py-8 shadow-sm sm:px-6 lg:px-8">
                <h2 className="text-3xl font-bold tracking-tight text-gray-900">Order overview</h2>
                <p className="mt-2 text-lg text-gray-600">
                    Here is a summary of the salsas you selected.
                </p>

                <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                    {orderItems.map((item) => (
                        <div key={item.item_name} className="rounded-2xl bg-white p-3 shadow-sm">
                            <img
                                alt={item.item_name}
                                src={item.image_url}
                                className="aspect-square w-full rounded-xl bg-gray-200 object-cover"
                            />
                            <div className="mt-4 flex justify-between gap-4">
                                <div>
                                    <h3 className="text-base font-semibold text-gray-900">{item.item_name}</h3>
                                    <p className="mt-1 text-base text-gray-500">{item.spice_level}</p>
                                    <p className="mt-1 text-base text-gray-500">
                                        {item.quantity} x {item.price} NOK
                                    </p>
                                </div>
                                <p className="shrink-0 text-base font-medium text-gray-900">
                                    {item.quantity * item.price} NOK
                                </p>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="mt-8 rounded-2xl bg-red-50 p-5">
                    <div className="flex justify-between text-lg text-gray-700">
                        <span>Total items</span>
                        <span>{totalItems}</span>
                    </div>
                    <div className="mt-3 flex justify-between text-2xl font-bold text-gray-900">
                        <span>Total</span>
                        <span>{totalPrice} NOK</span>
                    </div>
                </div>

                <button
                    type="button"
                    onClick={onBack}
                    className="mt-8 w-full rounded-xl bg-red-600 py-4 text-xl font-semibold text-white hover:bg-red-700"
                >
                    Back to salsas
                </button>
            </main>
        </div>
    );
}

function CartTotal({
    totalItems,
    totalPrice
}: {
    totalItems: number;
    totalPrice: number;
}) {
    return (
        <div className="flex justify-end">
            <div className="relative rounded-md bg-white px-5 py-3 pr-6 shadow-md">
                <span className="absolute -right-2 -top-2 flex h-7 w-7 items-center justify-center rounded-md bg-red-600 text-base font-bold text-white">
                    {totalItems}
                </span>
                <div className="flex items-center gap-3">
                    <span className="text-xl">🛒</span>
                    <div className="text-right">
                        <p className="text-sm font-semibold uppercase tracking-wide text-gray-500">
                            Cart
                        </p>
                        <p className="text-base font-bold text-gray-900">
                            {totalPrice} NOK
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}


function CardCounter({
    amount,
    onDecrease,
    onIncrease,
}: {
    amount: number;
    onDecrease: () => void;
    onIncrease: () => void;
}) {
    return (
        <div className="mt-5 flex items-center justify-between rounded-md bg-red-50 p-2">
            <button
                type="button"
                onClick={onDecrease}
                className="h-9 w-9 rounded-md bg-red-600 text-xl font-bold text-white shadow hover:bg-red-700"
            >
                -
            </button>
            <span className="min-w-10 text-center text-xl font-bold text-gray-900">
                {amount}
            </span>
            <button
                type="button"
                onClick={onIncrease}
                className="h-9 w-9 rounded-md bg-red-600 text-xl font-bold text-white shadow hover:bg-red-700"
            >
                +
            </button>
        </div>
    );
}

export default App;
