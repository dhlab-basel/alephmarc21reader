import abc

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class AbstractAlephMarcReader(ABC):

    class Person:
        """
        Represents a person.
        :param str|False name: the name of the person (family name, first name), if any.
        :param str|False lifespan: the lifespan of the person (year of birth and death separated by a '-'), if any.
        :param str|False gnd: the GND of the person, otherwise 'no_GND', if any.
        :param str|False role: the role of the person (author etc.), if any.

        """

        def __init__(self, name, lifespan, gnd, role):
            self.name = name
            self.lifespan = lifespan
            self.gnd = gnd
            self.role = role

    class Place:
        """
        Represents a place.
        :param str|False name: the name of the place, if any.
        :param str|False gnd: the GND of the place, otherwise 'no_GND', if any.
        """

        def __init__(self, name, gnd):
            self.name = name
            self.gnd = gnd

    class Shelfmark:
        """
        Represents a shelfmark.
        :param str|False institution: the name of the institution, if any.
        :param str|False identifier: the identifier, if any.
        """
        def __init__(self, institution, identifier):
            self.institution = institution
            self.identifier = identifier

    def __init__(self, gnd_index):
        """
        :param gnd_index: index of the GND subfield.
        """
        self._gnd_index = gnd_index

    @abc.abstractmethod
    def __get_subfield_text(self, marc_field, index):
        pass

    @abc.abstractmethod
    def __get_field(self, index):
        pass

    def _get_person_info(self, marc_field, gnd_index):
        """
        Extracts person information from a Marc field incl. the GND, if any.
        Returns a dictionary containing that information with they keys: GND, name, date, role.
        :param pymarc.field.Field marc_field: the Marc21 field that contains information about a person.
        :param str gnd_index: the index of the GND subfield.
        :return: Person
        """

        name = self.__get_subfield_text(marc_field, 'a')

        date = self.__get_subfield_text(marc_field, 'd')

        gnd = self.__get_subfield_text(marc_field, gnd_index).replace(',', '') # get rid of trailing comma

        role = self.__get_subfield_text(marc_field, '4')

        return self.Person(name, date, gnd, role)

    def get_author(self):
        """
        Returns information about the author.
        :return: [Person]
        """
        author = []
        for field in self.__get_field('100'):
            author.append(self._get_person_info(field, self._gnd_index))

        # check for recipients (700) that are actually authors
        for field in self.__get_field('700'):
            person = self._get_person_info(field, self._gnd_index)

            if person.role == "aut":
                author.append(person)

        return author
    get_author.__annotations__ = {'return': [Person]}

    def get_recipient(self):
        """
        Returns information about the recipient.
        :return: [Person]
        """
        recipient = []
        for field in self.__get_field('700'):
            person = self._get_person_info(field, self._gnd_index)

            if person.role == "rcp":
                recipient.append(person)

        return recipient
    get_recipient.__annotations__ = {'return': [Person]}

    def get_mentioned_person(self):
        """
        Returns information about a mentioned person.
        :return: [Person]
        """
        mentioned = []
        for field in self.__get_field('600'):
            mentioned.append(self._get_person_info(field, self._gnd_index))

        return mentioned
    get_mentioned_person.__annotations__ = {'return': [Person]}

    def get_date(self):
        """
        Returns the date.
        :return: [str]
        """
        date = []
        for field in self.__get_field('046'):
            date_text = self.__get_subfield_text(field, 'c')

            if date_text:
                date.append(date_text)

        return date
    get_date.__annotations__ = {'return': [str]}

    def get_creation_place(self):
        """
        Returns the place of creation.
        :return: [Place]
        """
        creation_place = []

        elements = self.__get_field('751')

        for element in elements:
            name = self.__get_subfield_text(element, 'a')

            gnd = self.__get_subfield_text(element, self._gnd_index)

            cp = self.Place(name, gnd)
            creation_place.append(cp)

        return creation_place
    get_creation_place.__annotations__ = {'return': [Place]}

    def get_shelfmark(self):
        """
        Returns the shelfmark.
        :return: [Shelfmark]
        """
        shelfmark = []

        elements = self.__get_field('852')

        for element in elements:
            institution = self.__get_subfield_text(element, 'a')

            identifier = self.__get_subfield_text(element, 'p')

            sm = self.Shelfmark(institution, identifier)
            shelfmark.append(sm)

        return shelfmark
    get_shelfmark.__annotations__ = {'return': [Shelfmark]}

    def get_footnote(self):
        """
        Returns the footnote.
        :return: [str]
        """
        footnote = []

        elements = self.__get_field('500')

        for element in elements:
            footnote_text = self.__get_subfield_text(element, 'a')

            if footnote_text:
                footnote.append(footnote_text)

        return footnote
    get_footnote.__annotations__ = {'return': [str]}