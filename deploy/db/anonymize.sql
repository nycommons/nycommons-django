--
-- Attempt to anonymize the database to make it suitable for sharing with other
-- developers.
--
-- Not very much personal data is stored by NYCommons:
-- * Organizers names, phone, email, and ediing URLs
-- * Admin users' password hashes
--
-- Everything else is publicly visible on the site.
--

-- Mask organizers' names, phone numbers, email addresses, and urls (where they 
-- can edit their organizing status)
update organize_organizer set name = 'Organizer ' || id, phone = '212555' || 1000 + id, email = 'organizer' || id || '@nycommons.org', url = 'organizer' || id;

-- Set user password hashes to NULL to avoid leaking
update auth_user set password = 'xxx';
