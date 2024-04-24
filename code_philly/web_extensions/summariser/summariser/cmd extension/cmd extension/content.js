console.log("hi")

const TOGETHER_API_KEY = 'd8a862be1d6e188397b852ad822990891a6ace0294873aac6c2ce8d6e34d0438'; 

var paragraph;
var paragraphs;


chrome.runtime.onMessage.addListener(gotMessage);

async function gotMessage(message, sender, sendResponse) {
    console.log(message);
    const paragraphs = document.querySelectorAll('p');

    for (let i = 0; i < paragraphs.length; i++) {
        const paragraph = paragraphs[i];

        if (paragraph.textContent.length > 150) {
            try {
                await processParagraph(message, paragraph.textContent, paragraph);
                await sleep(1000); // Sleep for 1 seconds between requests
            } catch (error) {
                console.error('Error processing paragraph:', error);
            }
        }
    }
}

async function processParagraph(message, paragraphText, paragraph) {
    paragraph=paragraph
    const response = await fetch('https://api.together.xyz/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${TOGETHER_API_KEY}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": [
                {"role": "system", "content": message},
                {"role": "user", "content": paragraphText}
            ]
        })
    });

    const data = await response.json();
    updatingText(data, paragraphText, paragraph);
}

function updatingText(data, paragraphText, paragraph) {
    paragraph=paragraph
    console.log(data.choices[0].message.content);
    paragraph.textContent = data.choices[0].message.content;
    console.log('done');
    console.log(paragraph)
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}



