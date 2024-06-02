
c.execute('''CREATE TABLE IF NOT EXISTS cruises
            (id, Price, Location, Dates, ton, shipURL, shipName)''')

(1,$199,Sydney;Brisbane,NA,92720,https://www.carnival.com/cruise-ships/carnival-luminosa, CARNIVAL LUMINOSA)
(2,$359,Los Angeles;Ensenada;Cabo San Lucas,NA,135156,https://www.carnival.com/cruise-ships/carnival-firenze, carnival firenze)
(3, 499, 'Miami;Cozumel;Key West', NULL, 110000, 'https://www.royalcaribbean.com/cruise-ships/symphony-of-the-seas', 'symphony of the seas'),
(4, 699, 'Barcelona;Palma de Mallorca;Florence', NULL, 139000, 'https://www.ncl.com/cruise-ships/norwegian-epic', 'norwegian epic'),
(5, 399, 'Galveston;Cozumel;Progreso', NULL, 128000, 'https://www.carnival.com/cruise-ships/carnival-breeze', 'carnival breeze'),
(6, 599, 'New York;San Juan;St. Thomas', NULL, 169379, 'https://www.royalcaribbean.com/cruise-ships/anthem-of-the-seas', 'anthem of the seas'),
(7, 549, 'Seattle;Juneau;Skagway', NULL, 116000, 'https://www.hollandamerica.com/cruise-ships/ms-noordam', 'ms noordam'),
(8, 799, 'Fort Lauderdale;Nassau;CocoCay', NULL, 168666, 'https://www.royalcaribbean.com/cruise-ships/freedom-of-the-seas', 'freedom of the seas'),
(9, 459, 'San Francisco;Victoria;Vancouver', NULL, 142000, 'https://www.princess.com/cruise-ships/majestic-princess', 'majestic princess'),
(10, 629, 'Miami;Grand Cayman;Jamaica', NULL, 133500, 'https://www.carnival.com/cruise-ships/carnival-vista', 'carnival vista'),
(11, 679, 'Sydney;Auckland;Wellington', NULL, 167800, 'https://www.celebritycruises.com/cruise-ships/celebrity-eclipse', 'celebrity eclipse');
