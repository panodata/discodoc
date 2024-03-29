##################
discodoc changelog
##################


in progress
===========


2019-08-13 0.3.0
================
- To respect privacy, skip all whisper posts when collecting cooked HTML fragments
- More detailed logging of post details while processing posts
- Adjust margin size to 2cm when converting with pandoc
- Rename "--path" parameter to "--output-path"
- Propagate topic creation/update date to pandoc metadata
- Add basic multi-topic rendering
- Add "--enumerate" option to prefix output filename with sequence number
- Add "--combine" option to assemble content from
  multiple topics into a single document


2019-08-12 0.2.0
================
- Make sure all posts of given topic will be fetched (up to 1000 for now).
- Add Discourse Api-Key authentication against hitting anonymous rate limits
- Improve documentation
- Add "--renderer" option for adjusting rendering with "--format=pdf|html"
- Add basic sandbox resource acquisition for assets required for HTML-based presentation/slideshow


2019-08-12 0.1.0
================
- Add project files
- Add command line interface


2019-08-11 0.0.0
================
- Initial commit, basic functionality
