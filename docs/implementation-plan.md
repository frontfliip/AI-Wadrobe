# Staged implementation plan

## Working sequence

Discuss the next sub-stage and its important decisions with the user, implement
only that sub-stage, verify it, then stop for review. This roadmap is not blanket
authorization to implement every stage.

Current progress: Stages 1.1 through 1.3 complete. Stage 1.4 is next, pending user
review. Preferences are an optional free-text note; saved outfits may be incomplete
but contain at least one clothing item. Private wardrobe ownership and the future
verified-public-product boundary are agreed. Shared products distinguish model
and color, not size. Verification mechanisms will be selected before sharing
implementation.

## Stage 1 - Foundation

- **1.1 Complete:** archive the previous scaffold, save the agreed plan/rules,
  and prepare a clean package structure. No routes or database implementation.
- **1.2 Complete:** agree on fields and relationships for the local user
  profile, private clothing items, image assets, outfits, and generated results.
  Document the future boundary for public outfits and verified shared products:
  unrestricted private uploads, verified identity required for public garments,
  reuse of existing products, and explicit saving. Implement records only as
  their functionality is needed; sharing remains deferred.
- **1.3 Complete:** minimal Flask `create_app`, environment-based data-directory
  setting, `GET /health` returning JSON, and one API test. No database or media
  directory is created by this stage.
- **1.4:** add SQLite initialization and persistence for the single local profile.
  Establish the local media directory; do not implement uploads yet.

Completion: the API starts and profile data survives an application restart.

## Stage 2 - Usable wardrobe

- **2.1:** choose the image-processing library and upload limits; implement a
  validated photo upload with manually supplied name and category.
- **2.2:** store the image and its clothing record; serve the stored image.
- **2.3:** list items, retrieve details, edit manual metadata, and filter by category.
- **2.4:** attach additional photos to an item and select its primary image.

Completion: upload a small wardrobe, browse its images, correct its details, and
retrieve everything after restart.

## Stage 3 - Clothing metadata

- **3.1:** prepare a small evaluation set with plain/patterned garments, different
  categories, and varied backgrounds.
- **3.2:** compare analysis approaches for category, colors, pattern, and
  style/formality. Discuss the results and select an approach with the user.
- **3.3:** implement an analysis call returning structured attribute suggestions;
  uncertain attributes can remain unknown.
- **3.4:** store suggestions, source information, confidence when available, and
  user corrections separately.
- **3.5:** add explicit reanalysis and filtering by the supported attributes.

Completion: useful metadata on the evaluation wardrobe; corrections persist and
are not overwritten by reanalysis.

## Stage 4 - Outfits and recommendations

- **4.1:** create, retrieve, list, and edit named outfits referencing clothing items.
  Allow incomplete saved combinations containing at least one clothing item.
- **4.2:** support top, bottom, dress, outerwear, shoes, and accessory roles; a dress
  can replace a top-and-bottom combination.
- **4.3:** define recommendation input: occasion/context and an optional required item.
- **4.4:** compare approaches on a small set of wardrobe/context examples, then
  discuss and select the recommendation mechanism.
- **4.5:** return several combinations with item references and short reasons;
  use available items and honor the required item.
- **4.6:** save a suggestion as an outfit and swap individual items.

Completion: recommend, explain, save, and edit outfits. Missing wardrobe pieces
produce an explanation rather than invented clothing.

## Stage 5 - Direct image-link imports

- **5.1:** fetch a direct image URL with URL validation and bounded size/time.
- **5.2:** reuse upload validation, storage, and analysis for the downloaded image.
- **5.3:** record the source URL and create the item as being considered, not owned.
- **5.4:** allow considered items in manually assembled outfits.
- **5.5:** recommend combinations around a selected candidate using owned items.
- **5.6:** allow a considered item to be marked as owned.

Completion: import, combine, save, and mark owned. Invalid links fail clearly
without leaving incomplete clothing records. Product-page scraping and text-only
shopping search are excluded.

## Stage 6 - First generated photos

- **6.1:** prepare reference outfits containing a selected top, bottom, and shoes.
- **6.2:** compare generation approaches, including lower-cost providers, for
  garment identity, color/pattern, shoe fidelity, anatomy, latency, and cost.
  Discuss the results and select an approach before integrating it.
- **6.3:** implement generation input using the three garment images and a
  fictional adult model description.
- **6.4:** generate one front-facing full-body image with all three selected items.
- **6.5:** store the output, exact input images, settings, and model information.
- **6.6:** retrieve results and support user-initiated regeneration; errors are
  explicit, with no automatic retry infrastructure.

Completion: retrieve generated photos and review whether all selected garments
remain recognizable across the evaluation outfits before expanding the feature.

## Stage 7 - Expanded photos

- **7.1:** add dresses, outerwear, then accessories; verify each addition separately.
- **7.2:** add front, side, back, and three-quarter view requests; explain when
  garment references do not establish unseen details.
- **7.3:** accept additional garment references if the chosen approach supports them.
- **7.4:** add an optional personal reference-photo mode and evaluate identity
  preservation separately.

Completion: supported combinations and views work on the evaluation examples;
unsupported requests receive a clear response.

## Verification and research checkpoints

- Add meaningful API and persistence tests for the behavior implemented in each
  sub-stage, including relevant failures.
- Use controlled substitutes for external services in ordinary tests; live
  calls belong to evaluation batches.
- Run relevant tests, Ruff lint, and Ruff formatting checks after final code edits.
- Treat approximately $10 as the first combined AI evaluation spending
  checkpoint. Report quality/cost findings and discuss further experiments.
- Technologies not listed in `architecture.md` remain unselected; ask before
  adding significant dependencies or services.

Video is a later roadmap item: animate an accepted outfit image after photo
generation is satisfactory. No video implementation subtasks are approved yet.
