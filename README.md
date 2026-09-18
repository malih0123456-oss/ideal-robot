# TRAUMA Phone Lookup API

Python/FastAPI project prepared for Vercel.

## API key

The default key is:

TRAUMA

You can later override it with a Vercel Environment Variable named:
TRAUMA_API_KEY

## Example

After deployment:

https://YOUR-DOMAIN.vercel.app/212612345678?key=TRAUMA

Also supported:

https://YOUR-DOMAIN.vercel.app/api/212612345678?key=TRAUMA

or:

https://YOUR-DOMAIN.vercel.app/api/lookup?number=212612345678&key=TRAUMA

Header alternative:

x-api-key: TRAUMA

## Deploy

1. Upload this ZIP to a GitHub repository.
2. Import the repository into Vercel.
3. Deploy with the project root unchanged.
4. Open the URL shown above.

No Node.js project is required. Vercel detects the Python function under api/.

## Notes

The API returns JSON with the phone number, detected country, and unique names returned by the configured upstream services.
