from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import *
from Products.Archetypes.references import HoldingReference
from Products.CMFCore.utils import getToolByName
from plone.app.folder.folder import ATFolder
from zope.interface import implements

from bika.lims import bikaMessageFactory as _
from bika.lims import config
from bika.lims.content.bikaschema import BikaFolderSchema
from bika.lims.interfaces import IStorageUnit

schema = BikaFolderSchema.copy() + Schema((
    StringField('Temperature',
                widget=StringWidget(
                    label=_('Temperature'),
                    input_class='numeric',
                ),
                ),
    ReferenceField('Department',
                   allowed_types=('Department',),
                   relationship='StorageUnitDepartment',
                   vocabulary='getDepartments',
                   referenceClass=HoldingReference,
                   widget=ReferenceWidget(
                       checkbox_bound=0,
                       label=_('Department'),
                       description=_('The laboratory department'),
                   ),
                   ),
    TextField('Address',
              default_output_type='text/plain',
              allowable_content_types=('text/plain',),
              widget=TextAreaWidget(
                  label=_('Address')),
              ),
))

schema['description'].schemata = 'default'
schema['description'].widget.visible = True


class StorageUnit(ATFolder):
    security = ClassSecurityInfo()
    implements(IStorageUnit)
    schema = schema

    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from bika.lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def getDepartments(self):
        bsc = getToolByName(self, 'bika_setup_catalog')
        result = []
        for r in bsc(portal_type='Department',
                     inactive_state='active'):
            result.append((r.UID, r.Title))
        return DisplayList(result)

    def getDepartmentTitle(self):
        return self.getDepartment() and self.getDepartment().Title() or ''


registerType(StorageUnit, config.PROJECTNAME)
