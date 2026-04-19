const DRIVER_DATA = {
    // Format: 'Full Name': { 
    //   number, teamColor, bgColor, textColor, wikiUrl }

    'Max Verstappen': {
        number: '1',
        teamColor: '#3671C6',
        bgColor: '#1E3A5F',
        textColor: '#ffffff',
        // This specific Wikipedia URL is verified working:
        wikiUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Max_Verstappen_2023_%28cropped%29.jpg/400px-Max_Verstappen_2023_%28cropped%29.jpg'
    },
    'Lewis Hamilton': {
        number: '44',
        teamColor: '#DC143C',
        bgColor: '#8B0000',
        textColor: '#ffffff',
        wikiUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Lewis_Hamilton_2016_Malaysia_2.jpg/400px-Lewis_Hamilton_2016_Malaysia_2.jpg'
    },
    'Charles Leclerc': {
        number: '16',
        teamColor: '#DC143C',
        bgColor: '#6B0000',
        textColor: '#ffffff',
        wikiUrl: null  // Wiki URL unreliable — use avatar
    },
    'Lando Norris': {
        number: '4',
        teamColor: '#FF8000',
        bgColor: '#7A3D00',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Carlos Sainz': {
        number: '55',
        teamColor: '#005AFF',
        bgColor: '#002080',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'George Russell': {
        number: '63',
        teamColor: '#00D2BE',
        bgColor: '#005A52',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Oscar Piastri': {
        number: '81',
        teamColor: '#FF8000',
        bgColor: '#7A3D00',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Fernando Alonso': {
        number: '14',
        teamColor: '#006F62',
        bgColor: '#003830',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Lance Stroll': {
        number: '18',
        teamColor: '#006F62',
        bgColor: '#003830',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Pierre Gasly': {
        number: '10',
        teamColor: '#0090FF',
        bgColor: '#003A70',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Alexander Albon': {
        number: '23',
        teamColor: '#005AFF',
        bgColor: '#002080',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Nico Hulkenberg': {
        number: '27',
        teamColor: '#B6BABD',
        bgColor: '#3A3A3A',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Esteban Ocon': {
        number: '31',
        teamColor: '#B6BABD',
        bgColor: '#3A3A3A',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Guanyu Zhou': {
        number: '24',
        teamColor: '#52E252',
        bgColor: '#1A4A1A',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Valtteri Bottas': {
        number: '77',
        teamColor: '#52E252',
        bgColor: '#1A4A1A',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Kimi Antonelli': {
        number: '12',
        teamColor: '#00D2BE',
        bgColor: '#005A52',
        textColor: '#000000',
        wikiUrl: null
    },
    'Jack Doohan': {
        number: '7',
        teamColor: '#0090FF',
        bgColor: '#003A70',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Liam Lawson': {
        number: '30',
        teamColor: '#3671C6',
        bgColor: '#1E3A5F',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Oliver Bearman': {
        number: '87',
        teamColor: '#E8002D',
        bgColor: '#6B0000',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Isack Hadjar': {
        number: '6',
        teamColor: '#1434CB',
        bgColor: '#0A1A70',
        textColor: '#ffffff',
        wikiUrl: null
    },
    'Gabriel Bortoleto': {
        number: '5',
        teamColor: '#52E252',
        bgColor: '#1A4A1A',
        textColor: '#ffffff',
        wikiUrl: null
    },
};

// Generate premium avatar URL for any driver
function getDriverAvatarUrl(name, bgColor, textColor) {
    const encoded = encodeURIComponent(name);
    const bg = (bgColor || '1a1a2e').replace('#', '');
    const fg = (textColor || 'e83a3a').replace('#', '');
    return `https://ui-avatars.com/api/?name=${encoded}&size=400&background=${bg}&color=${fg}&bold=true&font-size=0.28&format=png`;
}

// Get best available image for a driver
function getDriverImageUrl(driverName) {
    const data = DRIVER_DATA[driverName];
    if (!data) return getDriverAvatarUrl(driverName, '1a1a2e', 'e83a3a');
    if (data.wikiUrl) return data.wikiUrl;
    return getDriverAvatarUrl(
        driverName,
        data.bgColor,
        data.textColor
    );
}

// Apply to all driver images on page load
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-driver-name]').forEach(img => {
        const name = img.dataset.driverName;
        const data = DRIVER_DATA[name];

        if (!data) {
            // Fallback for anyone not in the list
            img.src = getDriverAvatarUrl(name, '1a1a2e', 'e83a3a');
            return;
        }

        // Try wiki URL first if available
        if (data.wikiUrl) {
            img.src = data.wikiUrl;
            img.onerror = function () {
                // Wiki failed — use avatar
                this.src = getDriverAvatarUrl(
                    name, data.bgColor, data.textColor
                );
                this.onerror = null; // Stop loop
            };
        } else {
            // Use avatar directly — more reliable
            img.src = getDriverAvatarUrl(
                name, data.bgColor, data.textColor
            );
            img.onerror = null;
        }
    });
});
