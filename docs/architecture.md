# Agreed architecture

## Foundation decisions

Agreed with the user on 2026-10-04:

- Fresh backend prototype, implemented one sub-stage at a time.
- Python, retaining the project's minimum supported version of 3.11.
- Flask for the API, chosen by the user.
- SQLite through Python's built-in `sqlite3` module for metadata and relationships.
- Local files for images; database records reference the files.
- One local user profile initially, without registration or login.

Use one application with ordinary modules. Module boundaries do not imply
separate deployments or microservices. Exact schemas and new dependencies are
discussed before the corresponding implementation step.

## Implemented application boundary (Stage 1.3)

`wardrobe_ai.create_app()` creates a Flask application with `GET /health`, which
returns HTTP 200 and `{"status": "ok"}`. This confirms the application responds;
it does not check database or external-service availability.

At application creation, `WARDROBE_DATA_DIR` is read from the environment, defaults
to `./data`, and is resolved relative to the launch directory. The resulting path
is stored in `app.config["DATA_DIR"]`. No dotenv loader, database connection, or
directory creation is included. Tests use Flask's built-in test client.

## Records and relationships

These are conceptual records, not an implemented database schema:

- A user profile has a display name, an optional free-text clothing-preference
  note, and private clothing items; person photos come later. Structured
  preference fields are not part of the initial version.
- A private clothing item belongs to exactly one user, is owned or being
  considered, and can have several images. A photo is sufficient; product name,
  brand, and product details are optional. Separate users' private uploads are
  separate records, even if they depict the same product.
- An image asset belongs to an item and records its local location and source.
- An outfit has a creator and references clothing rather than copying it. Its
  creator is not a restriction on future viewing or reuse by other people.
  Saved outfits can be incomplete, but must contain at least one clothing item.
  Outfit contents link items to roles such as top, bottom, and shoes; an item
  can appear in several outfits without duplicating its clothing record.
- A generated result records the selected outfit and the images/settings used.

Extracted attribute suggestions must not overwrite user corrections.

### Initial record contents

These describe the agreed data, not tables to create all at once:

| Record | Basic contents | Introduced with |
| --- | --- | --- |
| User profile | ID, display name, optional preference note | Stage 1.4 |
| Private clothing item | ID, user ID, optional name, category, owned/considering status, optional size, selected primary image | Stage 2 |
| Clothing image | ID, item ID, stored file location, optional source image URL | Stage 2; link sources in Stage 5 |
| Outfit | ID, creator ID, name, optional occasion/context | Stage 4 |
| Outfit contents | Outfit ID, clothing-item reference, garment role | Stage 4 |
| Generated result | ID, outfit reference, exact input image references, output location, model/settings | Stage 6 |

Additional clothing attributes follow the analysis work in Stage 3. Shared
products and their verification fields remain deferred until publishing work.
The future product association must not remove ownership from private items.

### Future publishing boundary

Publishing is deferred, but the agreed design separates unrestricted private
wardrobe records from verified shared products. Avoiding duplicate public product
records is a requirement:

- Publishing an outfit makes a public representation of the selected outfit and
  garment information; it does not expose the user's underlying wardrobe records.
- Every garment in a published outfit must resolve to a verified shared product
  identity. A private item can remain unidentified indefinitely, but it cannot
  be included in a public outfit until its product identity is established.
- Publishing reuses an existing shared product record where that verified
  identity already exists. A new public record is permitted only after identity
  verification and checking the shared products. Database uniqueness must enforce
  the agreed canonical identity to prevent duplicate records, including concurrent
  attempts to publish the same product.
- Other users and outfits reuse that shared product ID. Reusing it does not
  create another product or automatically save it into a user's wardrobe.
- Explicit saving creates a user-specific wardrobe record marked as considering,
  linked to the shared product. Saving does not imply ownership. Repeated saves
  of the same shared product by the same user must not create duplicate entries.
- Separate users can have their own private records linked to the same shared
  product. Private duplicate uploads need not be matched or merged.
- Shared product identity is at the verified model-and-color level. Different
  sizes of the same model and color share one product record; different colors
  are separate products. Size, when provided, belongs to the user's private
  wardrobe entry rather than defining another shared product.
- A direct image URL and a purchase URL are distinct. A descriptive name or
  similar appearance alone is not sufficient verification of exact identity.
- Accepted identity evidence and canonical identifiers must be agreed before
  implementing verification. Source identifiers must resolve to the agreed
  model-and-color identity rather than creating duplicates for different sizes.
  If identity cannot be established or reconciled, keep the item private rather
  than create an unidentified public record.

The earlier decision to allow unidentified public garments is superseded. No
shared-product tables, posting endpoints, feed, or verification mechanism are
implemented in this stage. The initial wardrobe remains user-specific.

### Different requirements for saving and generation

An incomplete outfit is a valid saved combination. The first generation feature
requires a selected top, bottom, and shoes with usable reference images. If a
required piece is missing, ask for it rather than inventing clothing. Completeness
rules for future publication are not yet selected; product verification is an
independent requirement for every garment that is included.

## Communication

The Flask API calls the relevant application logic directly:

1. Wardrobe operations read/write records and image files.
2. Image analysis reads stored images and returns attribute suggestions.
3. Recommendations read wardrobe items, context, and an optional required item;
   they return outfit proposals with explanations.
4. Link import downloads a direct image URL and uses the same ingestion logic as
   an uploaded file. The new item starts as being considered, not owned.
5. Photo generation reads selected garment images and stores the output together
   with its input references and generation details.

Initially, processing requests return a result or error directly. Persistent jobs,
queues, retry orchestration, and notifications are deferred. If a chosen provider
requires asynchronous result retrieval, discuss that constraint with the user
before changing this approach.

## First generation target

Generate one front-facing, full-body image of a fictional adult wearing a selected
top, bottom, and pair of shoes. Additional garment types, views, and personal
reference photos follow only after this works. Video is a later roadmap item.

## Deferred decisions and functionality

- AI providers/models and image-processing libraries: evaluate at their stages.
- Approximately $10 is the first combined AI evaluation spending checkpoint, not
  a permanent budget ceiling. Review findings with the user before further spend.
- Frontend/mobile application, authentication, access/deletion workflows, cloud
  hosting/storage, background-job tracking, and vector-search infrastructure.
- Public outfit posting, verified shared products, and identity verification:
  the private/public boundary above is agreed, but implementation is deferred.
- Retailer product-page extraction and text-only shopping search. Only direct
  image links are included in the initial importer.

The archived AWS architecture and FastAPI implementation are superseded; they
are not approved requirements for this prototype.
