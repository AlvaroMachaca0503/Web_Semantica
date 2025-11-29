import { useState } from 'react';

const CategoryFilter = ({ onFilterChange }) => {
    const [selectedCategory, setSelectedCategory] = useState('');

    const categories = [
        { value: '', label: 'Todas las categorías' },
        { value: 'Electrónica', label: '⚡ Electrónica' },
        { value: 'Smartphone', label: '📱 Smartphones' },
        { value: 'Laptop', label: '💻 Laptops' },
        { value: 'Hogar', label: '🏠 Hogar' },
        { value: 'Moda', label: '👔 Moda' },
    ];

    const handleChange = (e) => {
        const value = e.target.value;
        setSelectedCategory(value);
        onFilterChange({ category: value || undefined });
    };

    return (
        <div className="bg-white p-4 rounded-lg shadow-md">
            <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span>📂</span>
                <span>Categoría</span>
            </h3>

            <select
                value={selectedCategory}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
            >
                {categories.map((category) => (
                    <option key={category.value} value={category.value}>
                        {category.label}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default CategoryFilter;
