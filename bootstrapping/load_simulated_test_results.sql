use session;

DELIMITER $$

CREATE FUNCTION `GuidToBinary`(
    $Data VARCHAR(36)
) RETURNS binary(16)
DETERMINISTIC
NO SQL
BEGIN
    DECLARE $Result BINARY(16) DEFAULT NULL;
    IF $Data IS NOT NULL THEN
        SET $Data = REPLACE($Data,'-','');
        SET $Result =
            CONCAT( UNHEX(SUBSTRING($Data,7,2)), UNHEX(SUBSTRING($Data,5,2)),
                    UNHEX(SUBSTRING($Data,3,2)), UNHEX(SUBSTRING($Data,1,2)),
                    UNHEX(SUBSTRING($Data,11,2)),UNHEX(SUBSTRING($Data,9,2)),
                    UNHEX(SUBSTRING($Data,15,2)),UNHEX(SUBSTRING($Data,13,2)),
                    UNHEX(SUBSTRING($Data,17,16)));
    END IF;
    RETURN $Result;
END

$$
delimiter ;

ALTER TABLE `session`.`session` 
ADD COLUMN `original_key` VARBINARY(16) NULL AFTER `sim_stop`;

delimiter $$
-- drop procedure multiply_session_rows
create procedure multiply_session_rows(in num int)
begin
	declare i int default 0;
    while i < num do    
		INSERT INTO `session`.`session`
			(`_key`,
			`_efk_proctor`,
			`proctorid`,
			`proctorname`,
			`sessionid`,
			`status`,
			`name`,
			`description`,
			`datecreated`,
			`datebegin`,
			`dateend`,
			`serveraddress`,
			`reserved`,
			`datechanged`,
			`datevisited`,
			`clientname`,
			`_fk_browser`,
			`environment`,
			`sessiontype`,
			`sim_language`,
			`sim_proctordelay`,
			`sim_abort`,
			`sim_status`,
			`sim_start`,
			`sim_stop`,
			`original_key`)
			SELECT
				GuidToBinary(uuid()),
				_efk_proctor,
				proctorid,
				proctorname,
				concat('TM', i, '-', FLOOR(RAND() * 20000000)),
				status,
				name,
				description,
				datecreated,
				datebegin,
				dateend,
				serveraddress,
				reserved,
				datechanged,
				datevisited,
				clientname,
				_fk_browser,
				environment,
				sessiontype,
				sim_language,
				sim_proctordelay,
				sim_abort,
				sim_status,
				sim_start,
				sim_stop,
				_key
            FROM
				session
			WHERE
				original_key is null;
        

		set i = i + 1;
	end while;
end
$$
delimiter ;

call multiply_session_rows(70);


INSERT INTO `session`.`sessiontests`
	(`_fk_session`,
	`_efk_adminsubject`,
	`_efk_testid`,
	`iterations`,
	`opportunities`,
	`meanproficiency`,
	`sdproficiency`,
	`strandcorrelation`,
	`sim_threads`,
	`sim_thinktime`,
	`handscoreitemtypes`)
SELECT
	ss._key,
	st._efk_adminsubject,
	st._efk_testid,
	st.iterations,
	st.opportunities,
	st.meanproficiency,
	st.sdproficiency,
	st.strandcorrelation,
	st.sim_threads,
	st.sim_thinktime,
	st.handscoreitemtypes
FROM
	session ss
    join sessiontests st on st._fk_session = ss.original_key
;

 
ALTER TABLE `session`.`testopportunity` 
ADD COLUMN `original_key` VARBINARY(16) NULL AFTER `scoretuples`;
    
    
INSERT INTO `session`.`testopportunity`
	(`_efk_testee`,
	`_efk_testid`,
	`opportunity`,
	`_fk_session`,
	`_fk_browser`,
	`testeeid`,
	`testeename`,
	`stage`,
	`status`,
	`prevstatus`,
	`restart`,
	`graceperiodrestarts`,
	`datechanged`,
	`datejoined`,
	`datestarted`,
	`daterestarted`,
	`datecompleted`,
	`datescored`,
	`dateapproved`,
	`dateexpired`,
	`datesubmitted`,
	`datereported`,
	`comment`,
	`abnormalstarts`,
	`reportingid`,
	`xmlhost`,
	`maxitems`,
	`numitems`,
	`dateinvalidated`,
	`invalidatedby`,
	`daterescored`,
	`ft_archived`,
	`items_archived`,
	`subject`,
	`datepaused`,
	`expirefrom`,
	`scoringdate`,
	`scoremark`,
	`scorelatency`,
	`language`,
	`proctorname`,
	`sessid`,
	`_key`,
	`clientname`,
	`datedeleted`,
	`daterestored`,
	`_version`,
	`_efk_adminsubject`,
	`environment`,
	`_datewiped`,
	`issegmented`,
	`algorithm`,
	`customaccommodations`,
	`numresponses`,
	`insegment`,
	`waitingforsegment`,
	`windowid`,
	`dateforcecompleted`,
	`dateexpiredreported`,
	`mode`,
	`itemgroupstring`,
	`initialability`,
	`initialabilitydelim`,
	`itemstring`,
	`scorestring`,
	`scoretuples`,
    original_key)
select
	FLOOR(RAND() * 100000), -- op._efk_testee,
	op._efk_testid,
	op.opportunity,
	op._fk_session,
	op._fk_browser,
	op.testeeid,
	op.testeename,
	op.stage,
	op.status,
	op.prevstatus,
	op.restart,
	op.graceperiodrestarts,
	op.datechanged,
	op.datejoined,
	op.datestarted,
	op.daterestarted,
	op.datecompleted,
	op.datescored,
	op.dateapproved,
	op.dateexpired,
	op.datesubmitted,
	op.datereported,
	op.comment,
	op.abnormalstarts,
	op.reportingid,
	op.xmlhost,
	op.maxitems,
	op.numitems,
	op.dateinvalidated,
	op.invalidatedby,
	op.daterescored,
	op.ft_archived,
	op.items_archived,
	op.subject,
	op.datepaused,
	op.expirefrom,
	op.scoringdate,
	op.scoremark,
	op.scorelatency,
	op.language,
	op.proctorname,
	ss.sessionid,
	GuidToBinary(uuid()),
	op.clientname,
	op.datedeleted,
	op.daterestored,
	FLOOR(RAND() * 10000), -- op._version,
	op._efk_adminsubject,
	op.environment,
	op._datewiped,
	op.issegmented,
	op.algorithm,
	op.customaccommodations,
	op.numresponses,
	op.insegment,
	op.waitingforsegment,
	op.windowid,
	op.dateforcecompleted,
	op.dateexpiredreported,
	op.mode,
	op.itemgroupstring,
	op.initialability,
	op.initialabilitydelim,
	op.itemstring,
	op.scorestring,
	op.scoretuples,
    op._key
FROM 
	testopportunity op
    JOIN session ss ON op._fk_session = ss.original_key;
    
    
INSERT INTO `session`.`testeerelationship`
	(`_fk_testopportunity`,
	`tds_id`,
	`entitykey`,
	`context`,
	`_date`,
	`attributevalue`,
	`relationship`)
SELECT
	op._key,
	rl.tds_id,
	rl.entitykey,
	rl.context,
	rl._date,
	rl.attributevalue,
	rl.relationship
FROM
	testeerelationship rl
    JOIN testopportunity op ON rl._fk_testopportunity = op.original_key;

INSERT INTO `session`.`testeeaccommodations`
	(`acctype`,
	`accvalue`,
	`acccode`,
	`_date`,
	`allowchange`,
	`testeecontrol`,
	`_fk_testopportunity`,
	`isapproved`,
	`isselectable`,
	`segment`,
	`valuecount`,
	`recordusage`)
SELECT
	ac.acctype,
	ac.accvalue,
	ac.acccode,
	ac._date,
	ac.allowchange,
	ac.testeecontrol,
	op._key,
	ac.isapproved,
	ac.isselectable,
	ac.segment,
	ac.valuecount,
	ac.recordusage
FROM
	testeeaccommodations ac
    JOIN testopportunity op ON ac._fk_testopportunity = op.original_key;
    
    
INSERT INTO `session`.`testeeattribute`
	(`_fk_testopportunity`,
	`tds_id`,
	`attributevalue`,
	`context`,
	`_date`)
SELECT
	op._key,
	ta.tds_id,
	ta.attributevalue,
	ta.context,
	ta._date
FROM
	testeeattribute ta
    JOIN testopportunity op ON ta._fk_testopportunity = op.original_key;
    


INSERT INTO `session`.`testeeresponse`
	(`_fk_testopportunity`,
	`_efk_itsitem`,
	`_efk_itsbank`,
	`_fk_session`,
	`opportunityrestart`,
	`page`,
	`position`,
	`answer`,
	`scorepoint`,
	`format`,
	`isfieldtest`,
	`dategenerated`,
	`datesubmitted`,
	`datefirstresponse`,
	`response`,
	`mark`,
	`score`,
	`hostname`,
	`numupdates`,
	`datesystemaltered`,
	`isinactive`,
	`dateinactivated`,
	`_fk_adminevent`,
	`groupid`,
	`isselected`,
	`isrequired`,
	`responsesequence`,
	`responselength`,
	`_fk_browser`,
	`isvalid`,
	`scorelatency`,
	`groupitemsrequired`,
	`scorestatus`,
	`scoringdate`,
	`scoreddate`,
	`scoremark`,
	`scorerationale`,
	`scoreattempts`,
	`_efk_itemkey`,
	`_fk_responsesession`,
	`segment`,
	`contentlevel`,
	`segmentid`,
	`groupb`,
	`itemb`,
	`datelastvisited`,
	`visitcount`,
	`geosyncid`,
	`satellite`,
	`scoredimensions`)
SELECT
	op._key,
	tr._efk_itsitem,
	tr._efk_itsbank,
	op._fk_session,
	tr.opportunityrestart,
	tr.page,
	tr.position,
	tr.answer,
	tr.scorepoint,
	tr.format,
	tr.isfieldtest,
	tr.dategenerated,
	tr.datesubmitted,
	tr.datefirstresponse,
	tr.response,
	tr.mark,
	tr.score,
	tr.hostname,
	tr.numupdates,
	tr.datesystemaltered,
	tr.isinactive,
	tr.dateinactivated,
	tr._fk_adminevent,
	tr.groupid,
	tr.isselected,
	tr.isrequired,
	tr.responsesequence,
	tr.responselength,
	tr._fk_browser,
	tr.isvalid,
	tr.scorelatency,
	tr.groupitemsrequired,
	tr.scorestatus,
	tr.scoringdate,
	tr.scoreddate,
	tr.scoremark,
	tr.scorerationale,
	tr.scoreattempts,
	tr._efk_itemkey,
	tr._fk_responsesession,
	tr.segment,
	tr.contentlevel,
	tr.segmentid,
	tr.groupb,
	tr.itemb,
	tr.datelastvisited,
	tr.visitcount,
	tr.geosyncid,
	tr.satellite,
    tr.scoredimensions
FROM
	testeeresponse tr
    JOIN testopportunity op ON tr._fk_testopportunity = op.original_key
;


INSERT INTO `session`.`testopportunity_readonly`
	(`_efk_testee`,
	`_efk_testid`,
	`opportunity`,
	`_fk_session`,
	`_fk_browser`,
	`testeeid`,
	`testeename`,
	`stage`,
	`status`,
	`prevstatus`,
	`restart`,
	`graceperiodrestarts`,
	`datechanged`,
	`datejoined`,
	`datestarted`,
	`daterestarted`,
	`datecompleted`,
	`datescored`,
	`dateapproved`,
	`dateexpired`,
	`datesubmitted`,
	`datereported`,
	`comment`,
	`abnormalstarts`,
	`reportingid`,
	`odecreated`,
	`odereported`,
	`xmlhost`,
	`maxitems`,
	`numitems`,
	`numresponses`,
	`dateinvalidated`,
	`invalidatedby`,
	`daterescored`,
	`ft_archived`,
	`items_archived`,
	`subject`,
	`datepaused`,
	`accommodationstring`,
	`expirefrom`,
	`customaccommodations`,
	`language`,
	`proctorname`,
	`sessid`,
	`_fk_testopportunity`,
	`clientname`,
	`_version`,
	`_efk_adminsubject`,
	`insegment`,
	`waitingforsegment`,
	`windowid`,
	`environment`,
	`mode`)
SELECT
	ro._efk_testee,
	ro._efk_testid,
	ro.opportunity,
	ro._fk_session,
	ro._fk_browser,
	ro.testeeid,
	ro.testeename,
	ro.stage,
	ro.status,
	ro.prevstatus,
	ro.restart,
	ro.graceperiodrestarts,
	ro.datechanged,
	ro.datejoined,
	ro.datestarted,
	ro.daterestarted,
	ro.datecompleted,
	ro.datescored,
	ro.dateapproved,
	ro.dateexpired,
	ro.datesubmitted,
	ro.datereported,
	ro.comment,
	ro.abnormalstarts,
	ro.reportingid,
	ro.odecreated,
	ro.odereported,
	ro.xmlhost,
	ro.maxitems,
	ro.numitems,
	ro.numresponses,
	ro.dateinvalidated,
	ro.invalidatedby,
	ro.daterescored,
	ro.ft_archived,
	ro.items_archived,
	ro.subject,
	ro.datepaused,
	ro.accommodationstring,
	ro.expirefrom,
	ro.customaccommodations,
	ro.language,
	ro.proctorname,
	ro.sessid,
	op._key,
	ro.clientname,
	ro._version,
	ro._efk_adminsubject,
	ro.insegment,
	ro.waitingforsegment,
	ro.windowid,
	ro.environment,
	ro.mode
FROM
	testopportunity_readonly ro
    JOIN testopportunity op ON ro._fk_testopportunity = op.original_key
;
    
    
-- cleanup by removing added extra columns
ALTER TABLE `session`.`testopportunity` 
DROP COLUMN `original_key`;

ALTER TABLE `session`.`session` 
DROP COLUMN `original_key`;

