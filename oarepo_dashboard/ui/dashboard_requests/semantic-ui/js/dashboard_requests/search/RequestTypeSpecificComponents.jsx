import {
  LabelTypeEditRecord,
  LabelTypeDeleteRecord,
  LabelTypePublishRecord,
} from "./labels/TypeLabels";
import {
  PublishRecordIcon,
  DeleteRecordIcon,
  EditRecordIcon,
} from "./icons/TypeIcons";

export const requestTypeSpecificComponents = {
  [`RequestTypeLabel.layout.edit-published-record`]: LabelTypeEditRecord,
  [`RequestTypeLabel.layout.delete-published-record`]: LabelTypeDeleteRecord,
  [`RequestTypeLabel.layout.publish-draft`]: LabelTypePublishRecord,
  [`InvenioRequests.RequestTypeIcon.layout.edit-published-record`]:
    EditRecordIcon,
  [`InvenioRequests.RequestTypeIcon.layout.delete-published-record`]:
    DeleteRecordIcon,
  [`InvenioRequests.RequestTypeIcon.layout.publish-draft`]: PublishRecordIcon,
};
