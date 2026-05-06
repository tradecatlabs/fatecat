package com.airic.fortel.core.destiny;

import static org.junit.jupiter.api.Assertions.assertNotNull;

import java.util.Map;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import com.airic.fortel.core.calendar.util.Lunar;
import com.airic.fortel.core.destiny.config.Config;
import com.airic.fortel.core.destiny.config.Config.ConfigType;
import com.airic.fortel.core.model.Data.GroundTime;
import com.airic.fortel.core.model.Data.Sex;
import com.airic.fortel.core.model.Destiny;
import com.airic.fortel.core.model.Ground;
import com.airic.fortel.core.model.MajorStar;
import com.airic.fortel.core.model.MinorStar;
import com.airic.fortel.core.model.RuntimeInfo;
import com.airic.fortel.core.model.RuntimeInfo.RuntimeCategory;
import com.airic.fortel.core.model.StarReaction;

/**
 * The Class AppTest.
 */
public class DestinyTest {

	/**
	 * Test app.
	 */
	@DisplayName("Test create Destiny from Destiny Config")
	@Test
	public void testApp() {

		Config initConfig = new Config(ConfigType.SKY, Sex.M, 1952, 12, 15, false, GroundTime.getByName("寅").get());
		Destiny destiny = new Destiny(initConfig);
		System.out.println(destiny.toJsonString());
		
		assertNotNull(destiny);
		Map<RuntimeCategory, RuntimeInfo> runtimeInfoMap = RuntimeInfo.getRuntimeInfoMap(destiny,
				new Lunar(2017, 6, 24, false));

		RuntimeInfo tenYearRuntimeInfo = runtimeInfoMap.get(RuntimeCategory.TEN_YEAR);
		Assertions.assertEquals(tenYearRuntimeInfo.getRuntimeDestinyTempleGround(), Ground.getByDisplayName("巳").get());
		Assertions.assertEquals(tenYearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_CLOTH),
				Ground.getByDisplayName("卯").get());
		Assertions.assertEquals(tenYearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_CLEVER),
				Ground.getByDisplayName("午").get());
		Assertions.assertEquals(tenYearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_SKILL),
				Ground.getByDisplayName("申").get());
		Assertions.assertEquals(tenYearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_FAILURE),
				Ground.getByDisplayName("辰").get());
		Assertions.assertEquals(tenYearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_HINDER),
				Ground.getByDisplayName("寅").get());
		Assertions.assertEquals(tenYearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_HONOR),
				Ground.getByDisplayName("子").get());
		Assertions.assertEquals(tenYearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_HONOR2),
				Ground.getByDisplayName("申").get());
		Assertions.assertEquals(tenYearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_HORSE_CHANGE),
				Ground.getByDisplayName("亥").get());

		Assertions.assertEquals(tenYearRuntimeInfo.getRuntimeStarReactionMap().get(StarReaction.STAR_TO_TREASURE),
				MajorStar.MAJOR_STAR_COUNSELLOR);
		Assertions.assertEquals(tenYearRuntimeInfo.getRuntimeStarReactionMap().get(StarReaction.STAR_TO_POWER),
				MajorStar.MAJOR_STAR_LAW);
		Assertions.assertEquals(tenYearRuntimeInfo.getRuntimeStarReactionMap().get(StarReaction.STAR_TO_POSITION),
				MajorStar.MAJOR_STAR_EMPEROR);
		Assertions.assertEquals(tenYearRuntimeInfo.getRuntimeStarReactionMap().get(StarReaction.STAR_TO_PROBLEM),
				MajorStar.MAJOR_STAR_MOON);

		RuntimeInfo yearRuntimeInfo = runtimeInfoMap.get(RuntimeCategory.YEAR);
		Assertions.assertEquals(yearRuntimeInfo.getRuntimeDestinyTempleGround(), Ground.getByDisplayName("酉").get());
		Assertions.assertEquals(yearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_CLOTH),
				Ground.getByDisplayName("午").get());
		Assertions.assertEquals(yearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_CLEVER),
				Ground.getByDisplayName("酉").get());
		Assertions.assertEquals(yearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_SKILL),
				Ground.getByDisplayName("巳").get());
		Assertions.assertEquals(yearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_FAILURE),
				Ground.getByDisplayName("未").get());
		Assertions.assertEquals(yearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_HINDER),
				Ground.getByDisplayName("巳").get());
		Assertions.assertEquals(yearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_HONOR),
				Ground.getByDisplayName("亥").get());
		Assertions.assertEquals(yearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_HONOR2),
				Ground.getByDisplayName("酉").get());
		Assertions.assertEquals(yearRuntimeInfo.getRuntimeMinorStarsMap().get(MinorStar.MINOR_STAR_HORSE_CHANGE),
				Ground.getByDisplayName("亥").get());

		Assertions.assertEquals(yearRuntimeInfo.getRuntimeStarReactionMap().get(StarReaction.STAR_TO_TREASURE),
				MajorStar.MAJOR_STAR_MOON);
		Assertions.assertEquals(yearRuntimeInfo.getRuntimeStarReactionMap().get(StarReaction.STAR_TO_POWER),
				MajorStar.MAJOR_STAR_RECREATION);
		Assertions.assertEquals(yearRuntimeInfo.getRuntimeStarReactionMap().get(StarReaction.STAR_TO_POSITION),
				MajorStar.MAJOR_STAR_COUNSELLOR);
		Assertions.assertEquals(yearRuntimeInfo.getRuntimeStarReactionMap().get(StarReaction.STAR_TO_PROBLEM),
				MajorStar.MAJOR_STAR_MOUTH);

		System.out.println(runtimeInfoMap);

		Config destinyConfig = new Config(ConfigType.SKY, Sex.F, 1952, 12, 15, false, GroundTime.getByName("寅").get());
		destiny = new Destiny(destinyConfig);
		System.out.println(destiny.toJsonString());
	}

}
