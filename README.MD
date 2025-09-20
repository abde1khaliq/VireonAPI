
# Vireon API

A moderation API made with care & love by Abdelkhaliq, built for real-world impact. It leverages AI-driven analysis and detection, designed for scalability and open collaboration.
## Features

- 🔍 **Moderation**: powered by Gemini for deep content analysis
- 🧱 **Modular design**: plug-and-play components for flexible integration
- 📦 **Reproducible setup**: streamlined onboarding and isolated environments
- 🧠 **Educational tooling**: built for targeted use, not mass deployment
## Run Locally

*Simple and crystal-clear installation*

Clone the project

```bash
git clone https://github.com/bondo2-hub/VireonAPI.git
```

Go to the project directory

```bash
cd VireonAPI
```

Install dependencies

```bash
pipenv install -r requirements.txt
```

Or

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

Generate a SECRET_KEY

```bash
cd base/management
python3 generate_secret_key.py
```

- *Store your newly generated key in the `.env` file in the `SECRET_KEY` variable.*

Get your own GEMINI_API_KEY

- Since this project relies on gemini, you'll have to get an API Key and store it in the `env` file in the `GEMINI_API_KEY` variable.

Start the server

```bash
python manage.py migrate
python manage.py collectstatic # Admin & rest_framework static files (css,js)
python manage.py runserver
```

- After all these steps, your server should start with no interruptions or any problems.
## Quick Start (Optional)

I've made a file for quick API Text & image moderation and detection. Just for simple testing

```bash
python -m base.configuration.moderate --text "Your text here"    # Text moderation
python -m base.configuration.moderate --image "Your image_url here" # Image moderation
```

**Results** should be something like this:
```
{
    "violation": true (true or false),
    "harm_type": [profanity] (list of harm types),
    "confidence": 0.97 (float 0 to 1),
    "severity": "moderate",
    "reasoning": string (only include if violation is true),
}
```
## API Reference

#### Text Moderation Endpoint

```http
  POST /v1/analyze/content
```

| Parameter     | Type     | Description                                                                 |
| :------------ | :------- | :-------------------------------------------------------------------------- |
| `api_key`     | `string` | **Required.** Pass as `Authorization: Bearer YOUR_API_KEY` in request header |
| `user_input`  | `string` | **Required.** The text to be moderated |
| `image_url`  | `string` | **Required.** The image to be moderated |

- ⚠️ You must provide either user_input or image_url — not both. One is required, both are optional, and mixing them will throw an error.


- 📢 Vireon is shipped with a built-in interface — complete with descriptive documentation, feature previews, and live testing. No guesswork, no setup headaches. Just plug in your key and start moderating.
## FAQ

#### Q: Do I need an API key to use VireonAPI?

Yes. All requests must include your key in the header as:
Authorization: Bearer YOUR_API_KEY

#### Q: Can I send both text and image in one request?

Nope. You must send either user_input (text) or image_url — not both.
Each is optional, but one is required to trigger moderation.

#### Q: Is this meant for production use?

Not yet. VireonAPI is built for targeted educational and experimental use, not mass deployment.
It’s modular, transparent, and open to contributions — but not hardened for scale (yet).

#### Q: Can I contribute or customize the pipeline?

Absolutely. The architecture is plug-and-play.
Fork it, tweak it, submit a pull request — just keep it modular and testable.

## Contributing

Contributions are always welcome

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.
## Authors

- [@abdelkhaliq](https://www.github.com/bondo2-hub)
## Support

For support, email ahmedthek3@gmail.com. Or join or Discord server [Vireon HQ](https://discord.gg/pQTqppHmp8)
## Feedback

If you have any feedback, please reach out to us at ahmedthek3@gmail.com

Discord; `abde1khaliq._`

[VireonHQ Discord](https://discord.gg/pQTqppHmp8)

## License

[MIT](https://choosealicense.com/licenses/mit/)


![Logo](https://i.postimg.cc/CLJpsJm6/vireon-logo-emerald.png)

