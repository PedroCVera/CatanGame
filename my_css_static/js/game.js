console.log('JavaScript is connected!');

document.querySelectorAll('.target').forEach(target => {
    target.addEventListener('click', function() {
        // Change the class of the target element
        this.classList.remove('target');
        if (this.classList.contains('road')){
            this.classList.add("green")
        } else
            this.classList.add('yellow');

        // Find the parent hex element and log its ID to the console
        const hex = this.closest('.hex');
        if (hex) {
            console.log('Hex chosen:', hex.id);
        }
    });
});

function create_sheep_card() {
    let newSheepCard = document.createElement('li');

    // Add the 'roster-card' and 'sheep' classes to the new list item
    newSheepCard.classList.add('roster-card', 'sheep');
    return newSheepCard
}

let your_hand_sheep = document.getElementById('your-hand-sheep')

let sheep = create_sheep_card()
your_hand_sheep.appendChild(sheep)

// your_hand.remove()





class Game {
    constructor(gameId) {
        this.gameid = gameId;
        this._board = null
        this.initialize()
    }

    async initialize(){
        await this.startNewGame()
        for (let key in this._board) {
            if (this._board.hasOwnProperty(key)) {
                const value = this._board[key];
                const [resource, number] = value.split(' | ');

                const hexElement = document.getElementById(key);

                if (hexElement) {
                    if (resource === "desert") {
                        hexElement.className = `hex sand robber`;
                    } else {
                        hexElement.className = `hex ${resource}`;
                    }
                    const numberElement = hexElement.querySelector('.number');
                    if (numberElement) {
                        numberElement.className = `number ${number}`;
                    }
                }
            }
        }
        console.log(this._board)
    }


    // Example function to get game status
    async getGameStatus() {
        const endpoint = `game-status/${this.gameId}`;
        const result = await this.sendRequest(endpoint, 'GET');
        if (result) {
            console.log('Game status:', result);
        }
    }

    getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                return cookie.substring(name.length + 1, cookie.length);
            }
        }
        return '';
    }

    async startNewGame() {
        const url = '/game/new_game/';  // URL to your Django view
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()  // Include the CSRF token
                }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            this._board = data.board;

            console.log('Game created:', data);
        } catch (error) {
            console.error('Error creating game:', error);
        }
    }
}

let game = new Game()
